
// Rational number type that can silently overflow without warning.

struct orat {
	int numerator;
	int denominator;
	orat( int n, int d ) { this->numerator = n; this->denominator = d; }
	orat( int n ) { this->numerator = n; this->denominator = 1; }
	orat &operator=( const int &x ) {
		this->numerator = x; this->denominator = 1; return *this;
	}
	orat &operator+=( const orat &x) {
		numerator = numerator*x.denominator + denominator*x.numerator;
		denominator *= x.denominator;
		return *this;
	}
	orat &operator/=( const orat &x) {
		numerator *= x.denominator;
		denominator *= x.numerator;
		return *this;
	}
	orat &operator*=( const orat &x) {
		numerator *= x.numerator;
		denominator *= x.denominator;
		return *this;
	}
	bool operator==( const orat &x ) { // 1/2 = 2/4 = 4/8
		return denominator*x.numerator-numerator*x.denominator==0;
	}
};

int sign( const int &x ) { if (x>0) return 1; if (x<0) return -1; return 0; }

bool operator==( const orat &x, const orat &y ) { // 1/2 = 2/4 = 4/8
	return y.denominator*x.numerator-y.numerator*x.denominator==0;
}

const orat operator+( const orat &x, const orat &y ) {
	int newnum = x.numerator*y.denominator + x.denominator*y.numerator;
	int newdenom = x.denominator*y.denominator;
	return orat(newnum,newdenom);
}

const orat operator-( const orat &x, const orat &y ) {
	int newnum = x.numerator*y.denominator - x.denominator*y.numerator;
	int newdenom = x.denominator*y.denominator;
	return orat(newnum,newdenom);
}

const orat operator*( const orat &x, const orat &y ) {
	int newnum = x.numerator*y.numerator;
	int newdenom = x.denominator*y.denominator;
	return orat(newnum,newdenom);
}

const orat operator/( const orat &x, const orat &y ) {
	int newnum = x.numerator*y.denominator;
	int newdenom = x.denominator*y.numerator;
	return orat(newnum,newdenom);
}

/////////////////////////// end of implementation


/////////////// tests
// compile with g++ -Dorat_test orat.cc

#ifdef orat_test
#include <iostream>

std::ostream& operator<<( std::ostream &os, const orat &x ) {
	os << x.numerator << "/" << x.denominator;
	return os;
}

int main() {
	int i = 0;
	orat i2(0);
	for (int j = 0;j<100000000;j+=50) {
		if (i>0 && i+1000000 < 0) std::cout << "overflow\n";
		i += 1000000;
		i2 += 1000000;
		i2 /= 5;
		i2 *= 5;
		std::cout << i << "\n";
		std::cout << i2 << "\n";
		std::cout << (i == i2) << "\n";
	}
}
#endif

