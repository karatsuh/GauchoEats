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
#include <iostream>

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
	std::ifstream lineDLG("lineDLG.dat");
	std::ifstream capDLG("capDLG.dat");
	std::ifstream lineCarrillo("lineCarrillo.dat");
	std::ifstream capCarrillo("capCarrillo.dat");
	std::ifstream lineOrtega("lineOrtega.dat");
	std::ifstream capOrtega("capOrtega.dat");

	if (!(lineDLG.peek() == std::ifstream::traits_type::eof()) ){ //check if file is empty (nothing to read, Lambda will let the user know instead of displaying image)
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Line at DLG'\n";
		gp << "set output 'lineDLG.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
	 	gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'lineDLG.dat' using 1:2 with lines\n";
	}

	if (!(capDLG.peek() == std::ifstream::traits_type::eof())){
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Capacity at DLG'\n";
		gp << "set output 'capDLG.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
	 	gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'capDLG.dat' using 1:2 with lines\n";
	}

	if (!(lineCarrillo.peek() == std::ifstream::traits_type::eof())){
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Line at Carrillo'\n";
		gp << "set output 'lineCarrillo.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
	 	gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'lineCarrillo.dat' using 1:2 with lines\n";
	}

	if(!(capCarrillo.peek() == std::ifstream::traits_type::eof())){
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Capacity at Carrillo'\n";
		gp << "set output 'capCarrillo.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
	 	gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'capCarrillo.dat' using 1:2 with lines\n";
	}

	if(!(lineOrtega.peek() == std::ifstream::traits_type::eof())){
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Line at Ortega'\n";
		gp << "set output 'lineOrtega.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
	 	gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'lineOrtega.dat' using 1:2 with lines\n";
	}

	if(!(capOrtega.peek() == std::ifstream::traits_type::eof())){
		gp << "set terminal png size 720,480\n";
		gp << "set title 'Capacity at Ortega'\n";
		gp << "set output 'capOrtega.png'\n";
		gp << "set xlabel 'Time'\n";
		gp << "set ylabel 'Line'\n";
		gp << "set key off\n";
		gp << "set timefmt '%H:%M:%S'\n";
		gp << "set xdata time\n";
		gp << "set format x '%H:%M:%S'\n";
		gp << "plot 'capOrtega.dat' using 1:2 with lines\n";
	}
}


int main(){
	plotPng();
	return 0;
}
