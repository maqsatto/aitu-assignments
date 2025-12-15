package Shapes

const Pi = 3.14

type Circle struct {
	radius float64
}

func (c Circle) area() float64 {
	return c.radius * c.radius * Pi
}

func (c Circle) perimeter() float64 {
	return Pi * c.radius
}
