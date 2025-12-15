package main

import (
	"fmt"

	"github.com/maqsatto/assignment-1-ap/Library"
)

func main() {
	lib := Library.NewLibrary()
	booka := Library.Book{IsBorrowed: false, Title: "Book A", Author: "John Doe", ID: 1}
	bookb := Library.Book{IsBorrowed: false, Title: "Book B", Author: "John Alex", ID: 2}
	bookc := Library.Book{IsBorrowed: true, Title: "Book C", Author: "John Doe", ID: 3}
	lib.AddBook(booka)
	lib.AddBook(bookb)
	lib.AddBook(bookc)

	lib.BorrowBook(booka)

	availBooks := lib.ListAllBooks()

	for _, book := range availBooks {
		fmt.Println(book)
	}
}
