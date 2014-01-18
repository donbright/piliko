struct a;
struct b {
	a &y;
	b( a &_y ) : y(_y) {};
};
struct a {
	int x;
};

int main() {
	a A;
	A.x=5;
	b B(A);
	b B2(A);
	b B3(A);
}

