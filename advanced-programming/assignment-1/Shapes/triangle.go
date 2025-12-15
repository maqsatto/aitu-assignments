package Shapes

import "math"

type Triangle struct {
	aside float64
	bside float64
	cside float64
}

func (t Triangle) perimeter() float64 {
	return t.aside + t.bside + t.cside
}

func (t Triangle) area() float64 {
	p := t.perimeter() / 2
	return math.Round(math.Sqrt(p * (p - t.aside) * (p - t.bside) * (p - t.cside)))
}
