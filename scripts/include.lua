-- Pandoc filter for the manuscript build.
-- 1. A paragraph that is exactly `{{include tables/name.md}}` is replaced by that file's Markdown, so every table
--    comes from scripts/make_tables.py rather than being typed into paper.md.
-- 2. A hyphen directly before a digit at the start of a word becomes a true minus sign (U+2212), as AMA style asks.
-- 3. Divs of class table-notes are set in a smaller size in LaTeX output.
-- 5. In DOCX output, column widths follow the content: each column gets at least its longest unbreakable word or
--    number, and the rest of the text width is shared by content length, so values such as "<.001" never break.
--    The widths in tables/*.md suit the PDF's small type; Word sets tables in 10 pt (reference.docx, Compact style).
-- 4. In DOCX output, inline math that is a single symbol becomes plain text (Times New Roman has the Greek letters),
--    so it survives tools that drop Word equation objects; formulas stay as equations. LaTeX output keeps the math
--    because Latin Modern has no Greek text glyphs.

local function read_file(path)
  local f = assert(io.open(path, "r"), "include: cannot open " .. path)
  local text = f:read("a")
  f:close()
  return text
end

function Para(el)
  local text = pandoc.utils.stringify(el)
  local path = text:match("^{{include%s+(.-)}}$")
  if path then
    return pandoc.read(read_file(path), "markdown+smart").blocks
  end
end

function Str(el)
  local s = el.text:gsub("^%-(%d)", "\u{2212}%1"):gsub("([%(%[/])%-(%d)", "%1\u{2212}%2")
  if s ~= el.text then
    return pandoc.Str(s)
  end
end

function Div(el)
  if el.classes:includes("table-notes") and FORMAT:match("latex") then
    table.insert(el.content, 1, pandoc.RawBlock("latex", "\\begingroup\\footnotesize"))
    table.insert(el.content, pandoc.RawBlock("latex", "\\endgroup"))
    return el
  end
end

local SYMBOLS = {
  ["\\rho"] = { pandoc.Str("\u{03C1}") },
  ["\\alpha"] = { pandoc.Str("\u{03B1}") },
  ["\\Delta"] = { pandoc.Str("\u{0394}") },
  ["-"] = { pandoc.Str("\u{2212}") },
  ["100 \\times"] = { pandoc.Str("100\u{00A0}\u{00D7}") },
  ["w"] = { pandoc.Emph("w") },
  ["e"] = { pandoc.Emph("e") },
  ["B"] = { pandoc.Emph("B") },
  ["s_e"] = { pandoc.Emph("s"), pandoc.Subscript("e") },
  ["R_e"] = { pandoc.Emph("R"), pandoc.Subscript("e") },
}

function Math(el)
  if el.mathtype == "InlineMath" and FORMAT:match("docx") and SYMBOLS[el.text] then
    return SYMBOLS[el.text]
  end
end

local function cell_lengths(rows, need, pref, ncol)
  for _, row in ipairs(rows) do
    local c = 1
    for _, cell in ipairs(row.cells) do
      local span = cell.col_span or 1
      if span == 1 and c <= ncol then
        local text = pandoc.utils.stringify(cell.contents)
        for word in text:gmatch("%S+") do
          need[c] = math.max(need[c], utf8.len(word) or #word)
        end
        pref[c] = math.max(pref[c], utf8.len(text) or #text)
      end
      c = c + span
    end
  end
end

function Table(tbl)
  if not FORMAT:match("docx") then
    return nil
  end
  local ncol = #tbl.colspecs
  local need, pref = {}, {}
  for i = 1, ncol do
    need[i], pref[i] = 2, 2
  end
  cell_lengths(tbl.head.rows, need, pref, ncol)
  for _, body in ipairs(tbl.bodies) do
    cell_lengths(body.head, need, pref, ncol)
    cell_lengths(body.body, need, pref, ncol)
  end
  cell_lengths(tbl.foot.rows, need, pref, ncol)
  -- Widths as fractions of the 6.5 in text width (reference.docx: Letter, 1 in margins). Each column first gets room
  -- for its longest word at 10 pt (130 twips a character, enough for capitals and bold) plus the cell's left and right
  -- margins (216 twips); what is left is shared by how much longer the column's longest cell is than that word.
  local text_width, char_twips, padding = 9360, 130, 260
  local minimum, extra, min_total, extra_total = {}, {}, 0, 0
  for i = 1, ncol do
    minimum[i] = need[i] * char_twips + padding
    extra[i] = math.max(math.min(pref[i], 60) - need[i], 0)
    min_total = min_total + minimum[i]
    extra_total = extra_total + extra[i]
  end
  local spare = math.max(text_width - min_total, 0)
  local scale = math.min(1, text_width / min_total)
  for i = 1, ncol do
    local share = extra_total > 0 and spare * extra[i] / extra_total or spare / ncol
    tbl.colspecs[i] = { tbl.colspecs[i][1], (minimum[i] * scale + share) / text_width }
  end
  return tbl
end

return {
  { Para = Para },
  { Str = Str, Div = Div, Math = Math, Table = Table },
}
