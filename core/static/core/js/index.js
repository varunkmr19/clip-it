document.addEventListener('load', () => {
  collections = document.querySelectorAll('.collections_content_item')
  console.log(collections)

  collections.addEventListener('click', (e) => {
    console.log(e.target.id)
  })
})
