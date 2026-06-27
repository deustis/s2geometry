#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>

#include "s2/s2cap.h"
#include "s2/s2cell.h"
#include "s2/s2cell_id.h"
#include "s2/s2latlng_rect.h"
#include "s2/s2point.h"
#include "s2/s2region.h"

namespace py = pybind11;

void bind_s2region(py::module& m) {
  py::class_<S2Region>(m, "S2Region",
      "Abstract base class for two-dimensional regions on the unit sphere.\n\n"
      "Defines the interface for computing bounding approximations of a region.\n"
      "Concrete subtypes include S2Cap, S2Cell, and S2LatLngRect.")

      // Geometric operations
      .def("cap_bound", &S2Region::GetCapBound,
           "Return a bounding cap for this region. The bound may not be tight.")
      .def("rect_bound", &S2Region::GetRectBound,
           "Return a bounding lat/lng rectangle for this region. The bound may not be tight.")
      .def("cell_union_bound", [](const S2Region& self) {
               std::vector<S2CellId> cell_ids;
               self.GetCellUnionBound(&cell_ids);
               return cell_ids;
           },
           "Return a list of S2CellIds whose union covers this region.")
      .def("contains_cell",
           py::overload_cast<const S2Cell&>(&S2Region::Contains, py::const_),
           py::arg("cell"),
           "Return true if the region completely contains the given cell.")
      .def("may_intersect", &S2Region::MayIntersect, py::arg("cell"),
           "Return true if the region may intersect the given cell.\n\n"
           "Returns false only if the region definitely does not intersect.")
      .def("contains_point",
           py::overload_cast<const S2Point&>(&S2Region::Contains, py::const_),
           py::arg("p"),
           "Return true if the region contains the given point.\n\n"
           "p is generally required to be unit length.");
}
