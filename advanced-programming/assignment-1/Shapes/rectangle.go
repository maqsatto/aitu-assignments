package Shapes

type Rectangle struct {
	length float64
	width  float64
}

func (r Rectangle) area() float64 {
	return r.length * r.width
}

func (r Rectangle) perimeter() float64 {
	return 2*r.length + 2*r.width
}
