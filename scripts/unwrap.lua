-- For scripts/import_standards.py: drop the page's div and span wrappers, so the only raw HTML left in the Markdown is
-- the complex tables pandoc cannot write as pipe tables.
function Div(el)
  return el.content
end

function Span(el)
  return el.content
end
