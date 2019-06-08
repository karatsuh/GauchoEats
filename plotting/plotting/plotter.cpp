/*
#include "matplotlibcpp.h"
#include <iostream>
namespace plt = matplotlibcpp;

int main(){
	
  //plt::plot({1,3,2,4});
  //const char* filename = "./testPlot.png";
  //std::cout << "Saving result to " << filename << std::endl;;
  //plt::save(filename);
}

*/



#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

int main() {
    plt::plot({1,3,2,4});
    plt::show();
}
