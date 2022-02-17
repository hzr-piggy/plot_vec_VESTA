# plot_vec_VESTA
A function written in python3 to plot vectors (displacement or magnetic moment) in VESTA

## Usage  
plot_vec(vesta_file, vec_file,  
		cutoff = 0.1,  
		radius=0.5, color=[255,0,0], penetrate = True, add_atom_radius = False,  
		scale_factor = 1,  
		delim = None, vec_type = "Cart", lat = None,  
		output_suffix = "_vec")  
    
## Parameters:
**vesta_file: string**  
  A *.vesta file   
**vec_file: string**   
  A file containing vectors having dimensions of 3N*1 (or 1*3N) with delimiter=delim  
**cutoff: double, optional**  
  Angstrom below which vector will not show  
**radius: double, optional**  
  Set radius of vector  
**color: array-like dim = 1-by-3, [0-255], optional**  
  Set color of vector  
**penetrate: Bool, optional**  
  Set whether vector penetrate atom  
**add_atom_radius: Bool, optional**  
  Set whether to add atom radius to vector modulus  
**scale_factor: double, optional**  
  Scale vector in the figure  
**delim: char, optional**  
  Delimiter in the vec_file  
**vec_type: string, optional**  
  Type of vectors, can be "Cart" (Cartesian), "Lat" (Lattice vector notation [u v w], in reduced coord), or "Modulus" (Modulus along crystallographic axis). Default is 'Cart'.    
**lat: array-like, optional**  
  3-by-3 lattice parameter in Angstrom required if vec_type == 'Cart'
**output_suffix: string, optional**  
  Output suffix
![GeTe_example](https://github.com/hzr-piggy/plot_vec_VESTA/tree/main/example/GeTe_vec.png)
