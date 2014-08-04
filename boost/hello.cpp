#include <Python.h>
#include <boost/python.hpp>
#include <vector>
#include <iostream>

using namespace boost::python;
using namespace std;

class Foo
{
    friend ostream& operator<<(ostream& os, const Foo& obj);
};


ostream& operator<<(ostream& os, const Foo& obj)
{
    return os;
}

list make_list()
{
    list l;
    return l;
}

list make_list_vector()
{
    vector<Foo> x;
    for (int i=0; i<5; ++i)
    {
        x.push_back(Foo());
    }

    for (auto it : x)
    {
        cout << it;// << endl;
    }

    list l(x);
    return l;
}

template<class T>
struct VecToList
{
    static PyObject* convert(const std::vector<T>& vec)
    {
        boost::python::list* l = new boost::python::list();
        for(size_t i = 0; i < vec.size(); i++)
        {
            (*l).append(vec[i]);
        }
        return l->ptr();
    }
};

char const* greet()
{
	return "hello, world";
}

BOOST_PYTHON_MODULE(hello)
{
	def("greet", &greet);
    def("make_list", make_list);
    def("make_list_vector", make_list_vector);

    // register converters with boost
    to_python_converter<std::vector<int, std::allocator<int> >, VecToList<int> >();
    to_python_converter<std::vector<float, std::allocator<float> >, VecToList<float> >();
    to_python_converter<std::vector<Foo, std::allocator<Foo> >, VecToList<Foo> >();

    class_<Foo>("Foo", no_init);
}
