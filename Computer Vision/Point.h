#include <iostream>
#include <math.h>

using namespace std;

class Point {

private: double xValue, yValue;

public:

	Point(double x = 0.0, double y = 0.0){
		xValue = x;
		yValue = y;
	}

	double getX(){
		return xValue;
	}

	double getY(){
		return yValue;
	}

	double getDistance(Point other){
		double deltaX = xValue - other.getX();
		double deltaY = yValue - other.getY();
		double distance = sqrt(pow(deltaX,2) + pow(deltaY,2));
		return distance;
	}

	

	//add comparator here to allow for sorts
	//override current operator function

};

ostream& operator<<(ostream &Str, Point &v) 
{ 
	Str<<"("<<v.getX()<<", "<<v.getY()<<")";
	return Str;
}