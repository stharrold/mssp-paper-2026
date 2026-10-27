-- Pandoc filter for the manuscript build.
-- 1. A paragraph that is exactly `{{include tables/name.md}}` is replaced by that file's Markdown, so every table
--    comes from scripts/make_tables.py rather than being typed into paper.md.
-- 2. A hyphen directly before a digit at the start of a word becomes a true minus sign (U+2212), as AMA style asks.
-- 3. Divs of class table-notes are set in a smaller size in LaTeX output.

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

return {
  { Para = Para },
  { Str = Str, Div = Div },
}
