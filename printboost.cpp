#include <boost/version.hpp>
#include <iostream>
#include <iomanip>

int main()
{
    std::cout << "Boost "     
    << BOOST_VERSION / 100000     << "."  // major version
    << BOOST_VERSION / 100 % 1000 << "."  // minior version
    << BOOST_VERSION % 100                // patch level
    << std::endl;
    return 0;
}

