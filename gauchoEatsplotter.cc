//compile with:
//g++ -o gauchoEatsplotter gauchoEatsplotter.cc -lboost_iostreams -lboost_system -lboost_filesystem
// then execute ./gauchoEatsplotter for png's to generate

#include <fstream>
#include <vector>
#include <map>
#include <limits>
#include <cmath>
#include <cstdio>
#include <boost/tuple/tuple.hpp>
#include <boost/foreach.hpp>

// Warn about use of deprecated functions.
#define GNUPLOT_DEPRECATE_WARN
#include "gnuplot-iostream.h"

// http://stackoverflow.com/a/1658429
#ifdef _WIN32
	#include <windows.h>
	inline void mysleep(unsigned millis) {
		::Sleep(millis);
	}
#else
	#include <unistd.h>
	inline void mysleep(unsigned millis) {
		::usleep(millis * 1000);
	}
#endif

void pause_if_needed() {
#ifdef _WIN32
	// For Windows, prompt for a keystroke before the Gnuplot object goes out of scope so that
	// the gnuplot window doesn't get closed.
	std::cout << "Press enter to exit." << std::endl;
	std::cin.get();
#endif
}

// Tell MSVC to not warn about using fopen.
// http://stackoverflow.com/a/4805353/1048959
#if defined(_MSC_VER) && _MSC_VER >= 1400
#pragma warning(disable:4996)
#endif


void plotPng() {
	Gnuplot gp;

	gp << "set terminal png\n";

	gp << "set title 'Line at DLG'\n";
	gp << "set output 'lineDLG.png'\n";
	gp << "set xlabel 'Time'\n";
	gp << "set ylabel 'Line'\n";
	gp << "set key off\n";
	gp << "plot 'data.dat' with lines\n";

	// std::vector<double> y_pts;
	// for (double i = 0.0; i < 50.0;i+=1.0){
	// 	y_pts.push_back(i);
	// }
	//
	// gp << "set title 'Line at DLG'\n";
	// gp << "set output 'lineDLG.png'\n";
	// gp << "set xlabel 'Time'\n";
	// gp << "set ylabel 'Line'\n";
	// gp << "plot '-' with lines\n";
	// gp.send1d(y_pts);

}


int main(){
	plotPng();
	return 0;
}
