package Shapes

import "fmt"

type Shape interface {
	area() float64
	perimeter() float64
}

func ExTwo() {
	shapes := []Shape{
		Circle{3},
		Rectangle{10, 10},
		Square{5},
		Triangle{5, 5, 5},
	}
	for _, shape := range shapes {
		fmt.Printf("Shape type: %T\n", shape)
	}
}
