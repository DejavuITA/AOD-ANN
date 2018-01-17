from .ConstantsAndParameters import *
from .model import *

# define pure iterative loop
# should be the same as the pure iteration
def pure_iterative(init_values, parameters, set_of_equations, iteration_sett):
    errii  = iteration_sett[0] # get the error for which the loop is interrupted
    maxii  = iteration_sett[1] # get the maximum number of iteration for the loop
    
    ii = 0
    # dd[ 'iteration number', 'data class (Up/Us/Ut/...)']
    all_data = np.array([init_values]) # init values ~ ('Up', 'Us', 'Ut', 'ΔN', 'ΔT', 'Δω')
    
    ### execute first iteration and store data
    all_data = np.vstack([all_data, set_of_equations(init_values, parameters)])
    
    ### store new values
    
    # enter loop
    while (np.abs(all_data[-1,2]-all_data[-2,2]) >= errii) & (ii<=maxii):
        ii += 1
        
        ### put old data in vector, to become input of equations()
        old_var = all_data[-1,:]
        
        ### generate new values and store them
        all_data = np.vstack([all_data, set_of_equations(old_var, parameters)])
        #new_data = set_of_equations(init_values, parameters)
        #np.vstack([data, new_data])
        
    return (all_data, ii)

# define first genetic algorithm
# mixes the last two output values as inputs for the next step
# pure_iterative(...) should be the same as genetic2(..., type=0)
def genetic2(init_values, parameters, set_of_equations, iteration_sett):
    errii = iteration_sett[0] # get the error for which the loop is interrupted
    maxii = iteration_sett[1] # get the maximum number of iteration for the loop
    weight = iteration_sett[2] # get the weight of the history
    
    ii = 0
    # dd[ 'iteration number', 'data class (Up/Us/Ut/...)']
    all_data = np.array([init_values]) # init values ~ ('Up', 'Us', 'Ut', 'ΔN', 'ΔT', 'Δω')
    
    ### execute first iteration and store data
    all_data = np.vstack([all_data, set_of_equations(init_values, parameters)])
    
    ### store new values
    
    # enter loop
    while (np.abs(all_data[-1,2]-all_data[-2,2]) >= errii) & (ii<=maxii):
        ii += 1
        
        ### put old data in vector, to become input of equations()
        old_var = (1.0-weight)*all_data[-1,:] + weight*all_data[-2,:]
        
        ### generate new values and store them
        all_data = np.vstack([all_data, set_of_equations(old_var, parameters)])
    
    return (all_data, ii)

def next_algorithm():
    print("not implemented yet")

# map the inputs to the function blocks
options = {0 : pure_iterative,
           2 : genetic2,
           3 : next_algorithm,
}

def iterator(variables, parameters, system_to_solve = ñequations, type = 0, err_it = 1e-6, max_it = 5e2, weight = 0):
    return options[type](variables, parameters, system_to_solve, (err_it, max_it, weight))

#def equations(var, par):
#    # variables
#    oxUp, oxUs, oxUtot, oxΔN, oxΔT, oxΔω = var
#    # parameters
#    pωs, pωp, pω0, pEp, pEs, pτa, pτb, pτ0, p𝛾TH, p𝛾FC, pMCp, pn0, pn2, pdndT, pdndN, pdαdN, pβtpa, pΓ, pV, pVeff = par
#    # constants
#    # c0, ħ
#
#    xUp   = -1.0J*np.sqrt(2/pτa)*pEp/(-1.0J*(pωp-pω0-oxΔω)-(1/pτa+1/pτb+1/pτ0))
#    xUs   = -1.0J*np.sqrt(2/pτa)*pEs/(-1.0J*(pωs-pω0-oxΔω)-(1/pτa+1/pτb+1/pτ0))
#    xUtot = np.abs(xUp)**2 + np.abs(xUs)**2
#    
#    xΔN = c0**2*pβtpa/p𝛾FC / ( 2*ħ*pωp*pV*pVeff*np.power(pn0,2) ) *np.power(xUtot,2)
#    xΔT = 1/( p𝛾TH*pMCp ) * (2/pτ0 + pdαdN*c0*pΓ/pn0*xΔN + ( np.power(c0/pn0,2)*pβtpa )/pVeff *xUtot ) * xUtot
#    
#    xΔω_TOE  = (-2*pω0/pn0*pdndT)*pΓ*xΔT
#    xΔω_FC   = (-2*pω0/pn0*pdndN + 1.0J*pdαdN*c0/pn0)*pΓ*xΔN
#    xΔω_KERR = (-2*pω0*c0*pn2/np.power(pn0,2) + 1.0J*np.power(c0/pn0,2)*pβtpa)/pVeff*xUtot
#    xΔω = (xΔω_TOE + xΔω_FC + xΔω_KERR)
#    
#    return (xUp, xUs, xUtot, xΔN, xΔT, xΔω)
#
#def ñequations(var, par):
#    # variables
#    oxUp, oxUs, oxUtot, oxΔN, oxΔT, oxΔω = var
#    # normalized parameters
#    pωs, pωp, pω0, pEp, pEs, pτa, pτb, pτ0, p𝛾TH, p𝛾FC, pMCp, pn0, pn2, pdndT, pdndN, pdαdN, pβtpa, pΓ, pV, pVeff = par
#    # constants
#    # c0, ħ
#
#    xUp   = -1.0J*np.sqrt(2/pτa)*pEp/(-1.0J*(pωp-1.0-oxΔω)-(1/pτa+1/pτb+1/pτ0))
#    xUs   = -1.0J*np.sqrt(2/pτa)*pEs/(-1.0J*(pωs-1.0-oxΔω)-(1/pτa+1/pτb+1/pτ0))
#    xUtot = np.abs(xUp)**2 + np.abs(xUs)**2
#    
#    xΔN = pβtpa/p𝛾FC / ( 8*3.94507e-03*pωp*pV*pVeff*np.power(np.pi*pn0,2) ) *np.power(xUtot,2)
#    xΔT = 1/( p𝛾TH*pMCp ) * (2/pτ0 + pdαdN/(2*np.pi*pn0)*pΓ*xΔN + np.power(2*np.pi*pn0,-2)*pβtpa/pVeff *xUtot ) * xUtot
#    
#    xΔω_TOE  = (-2.0/pn0*pdndT)*pΓ*xΔT
#    xΔω_FC   = (-2.0/pn0*pdndN + 1.0J*pdαdN/(2*np.pi*pn0))*pΓ*xΔN
#    xΔω_KERR = (-2.0*pn2/(2*np.pi*np.power(pn0,2)) + 1.0J*np.power(2*np.pi*pn0,2)*pβtpa)/pVeff*xUtot
#    xΔω = (xΔω_TOE + xΔω_FC + xΔω_KERR)
#    
#    return (xUp, xUs, xUtot, xΔN, xΔT, xΔω)
#
#def system_eq(var, *par):
#    # variables
#    xUpR, xUpI, xUsR, xUsI, xUtot, xΔN, xΔT, xΔωR, xΔωI = var
#    # parameters
#    pωs, pωp, pω0, pEp, pEs, pτa, pτb, pτ0, p𝛾TH, p𝛾FC, pMCp, pn0, pn2, pdndT, pdndN, pdαdN, pβtpa, pΓ, pV, pVeff = par
#    # constants
#    # c0, ħ
#
#    fUpR = -xUpR - np.sqrt(2/pτa)*pEp * (pωp-pω0-xΔωR) / (np.power(pωp-pω0-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    fUpI = -xUpI - np.sqrt(2/pτa)*pEp * (1/pτa+1/pτb+1/pτ0+xΔωI) / (np.power(pωp-pω0-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    
#    fUsR = -xUsR - np.sqrt(2/pτa)*pEs * (pωs-pω0-xΔωR) / (np.power(pωs-pω0-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    fUsI = -xUsI - np.sqrt(2/pτa)*pEs * (1/pτa+1/pτb+1/pτ0+xΔωI) / (np.power(pωs-pω0-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    
#    fUt  = -xUtot+ xUpR**2 + xUpI**2 + xUsR**2 + xUsI**2
#    
#    fΔN  = -xΔN  + c0**2*pβtpa/p𝛾FC / ( 2*ħ*pωp*pV*pVeff*np.power(pn0,2) ) *np.power(xUtot,2)
#    fΔT  = -xΔT  + 1/( p𝛾TH*pMCp ) * (2/pτ0 + pdαdN*c0*pΓ/pn0*xΔN + ( np.power(c0/pn0,2)*pβtpa )/pVeff *xUtot ) * xUtot
#        
#    fΔωR = -xΔωR + (-2*pω0/pn0*pdndT)*pΓ*xΔT + (-2*pω0/pn0*pdndN) * pΓ*xΔN + (-2*pω0*c0*pn2/np.power(pn0,2)) / pVeff*xUtot
#    fΔωI = -xΔωI + (pdαdN*c0/pn0) * pΓ*xΔN + (np.power(c0/pn0,2)*pβtpa) / pVeff*xUtot
#    
#    return (xUpR, xUpI, xUsR, xUsI, xUtot, xΔN, xΔT, xΔωR, xΔωI)
#
#def ñsystem_eq(var, *par):
#    # variables
#    xUpR, xUpI, xUsR, xUsI, xUtot, xΔN, xΔT, xΔωR, xΔωI = var
#    # normalized parameters
#    pωs, pωp, pω0, pEp, pEs, pτa, pτb, pτ0, p𝛾TH, p𝛾FC, pMCp, pn0, pn2, pdndT, pdndN, pdαdN, pβtpa, pΓ, pV, pVeff = par
#    # constants
#    # c0, ħ
#
#    fUpR = -xUpR - np.sqrt(2/pτa)*pEp * (pωp-1-xΔωR) / (np.power(pωp-1-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    fUpI = -xUpI - np.sqrt(2/pτa)*pEp * (1/pτa+1/pτb+1/pτ0+xΔωI) / (np.power(pωp-1-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    
#    fUsR = -xUsR - np.sqrt(2/pτa)*pEs * (pωs-1-xΔωR) / (np.power(pωs-1-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    fUsI = -xUsI - np.sqrt(2/pτa)*pEs * (1/pτa+1/pτb+1/pτ0+xΔωI) / (np.power(pωs-1-xΔωR, 2)+np.power(1/pτa+1/pτb+1/pτ0+xΔωI,2))
#    
#    fUt  = -xUtot+ xUpR**2 + xUpI**2 + xUsR**2 + xUsI**2
#    
#    fΔN  = -xΔN  + pβtpa/p𝛾FC / ( 8*3.94507e-03*pωp*pV*pVeff*np.power(np.pi*pn0,2) ) *np.power(xUtot,2)
#    fΔT  = -xΔT  + 1/( p𝛾TH*pMCp ) * (2/pτ0 + pdαdN/(2*np.pi*pn0)*pΓ*xΔN + np.power(2*np.pi*pn0,-2)*pβtpa/pVeff *xUtot ) * xUtot
#
#    fΔωR = -xΔωR + (-2.0/pn0*pdndT)*pΓ*xΔT + (-2.0/pn0*pdndN)*pΓ*xΔN + (-2.0*pn2/(2*np.pi*np.power(pn0,2)))/pVeff*xUtot
#    fΔωI = -xΔωI + (pdαdN/(2*np.pi*pn0))*pΓ*xΔN + (np.power(2*np.pi*pn0,2)*pβtpa)/pVeff*xUtot
#    
#    return (xUpR, xUpI, xUsR, xUsI, xUtot, xΔN, xΔT, xΔωR, xΔωI)