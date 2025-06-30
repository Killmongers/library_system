async function loadBooks() {
    const res = await fetch('/books');
    const books = await res.json();

    const list = document.getElementById('book-list');
    list.innerHTML = "";

    books.forEach(book => {
        const div = document.createElement('div');
        div.innerHTML = `
            <strong>${book.title}</strong> by ${book.author} 
            - ${book.available ? '✅ Available' : '❌ Borrowed'}
            ${book.available 
                ? `<button onclick="borrowBook(${book.id})">Borrow</button>` 
                : `<button onclick="returnBook(${book.id})">Return</button>`}
            <hr/>
        `;
        list.appendChild(div);
    });
}

async function addBook() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;

    await fetch('/books', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, author})
    });

    document.getElementById('title').value = "";
    document.getElementById('author').value = "";

    loadBooks();
}

async function borrowBook(id) {
    await fetch(`/books/${id}/borrow`, {method: 'POST'});
    loadBooks();
}

async function returnBook(id) {
    await fetch(`/books/${id}/return`, {method: 'POST'});
    loadBooks();
}

// Load books on page load
window.onload = loadBooks;

