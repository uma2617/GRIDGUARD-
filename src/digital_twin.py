def digital_twin_sim(solar, wind, load, soc):
    generation = solar + wind
    net = generation - load
    if net > 0:
        charge = min(net, 20)
        new_soc = min(95, soc + charge*0.2)
        grid_flow = net - charge
        status = "Excess Power - Charging Battery"
    else:
        discharge = min(abs(net), 20)
        new_soc = max(10, soc - discharge*0.2)
        grid_flow = net + discharge
        status = "Deficit - Battery Discharging"
    return generation, net, new_soc, grid_flow, status