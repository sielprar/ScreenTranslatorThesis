local function loosen(list)
  for i, item in ipairs(list.content) do
    list.content[i] = item:walk({
      Plain = function(el) return pandoc.Para(el.content) end,
    })
  end
  return list
end

return {
  { BulletList = loosen, OrderedList = loosen },
}
