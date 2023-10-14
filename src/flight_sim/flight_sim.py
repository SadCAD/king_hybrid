"""
SETTING UP A SIM WITH ROCKETPY
DEFINE ENVIRONMENT --> DEFINE MOTOR --> DEFINE ROCKET
RUNNING SIM BY DEFINING FLIGHT OBJECT
PLOTTING AT THE END
"""

#TODO: ADD import src.constants

from rocketpy import (
    Environment,
    Rocket,
    Flight,
    HybridMotor,
    Fluid,
    CylindricalTank,
    MassFlowRateBasedTank,

)

#1) def environment
env = Environment(latitude=47.989083, longitude=-81.853361, elevation=370.3) #LAUNCH PAD DATA FOR LAUNCH CANADA

env.set_date(
    (2023, 10, 14, 00)
)  # Hour given in UTC time #Arbitrary Date

env.set_atmospheric_model(type="Forecast", file="GFS") #THIS USES GFS ATMOSPHERIC MODEL, OTHER MODELS EXIST CAN BE LOOKED AT LATER
#env.info() #PRINTS ENVIRONMENT DATA

#2) Define ENGINE! START W TANK THEN CC

# Define the fluids
oxidizer_liq = Fluid(name="N2O_l", density=1220)
oxidizer_gas = Fluid(name="N2O_g", density=1.9277)

# Define tank geometry
tank_shape = CylindricalTank(115 / 2000, 0.705)

# Define tank
oxidizer_tank = MassFlowRateBasedTank(
    name="oxidizer tank",
    geometry=tank_shape,
    flux_time=5.2,
    initial_liquid_mass=4.11,
    initial_gas_mass=0,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=r'./src/m_dot_ox.csv',
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=oxidizer_liq,
    gas=oxidizer_gas,
)

#COMBUSTION CHAMBER
example_hybrid = HybridMotor(
    thrust_source=r'./src/thrust.csv',
    dry_mass=2,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=63.36 / 2000,
    grain_number=4,
    grain_separation=0,
    grain_outer_radius=0.0575,
    grain_initial_inner_radius=0.025,
    grain_initial_height=0.1375,
    grain_density=900,
    grains_center_of_mass_position=0.384,
    center_of_dry_mass_position=0.284,
    nozzle_position=0,
    burn_time=5.2,
    throat_radius=26 / 2000,
)

#ADD THE OX TANK TO THE CC
example_hybrid.add_tank(
  tank = oxidizer_tank, position = 1.0115
)

#NOW WE HAVE OUR HYBRID, CAN SEE RESULTS W example_hybrid.all_info()

#NOW WE DEFINE THE ROCKET:
"""
Define the rocket itself by passing in the rockets dry mass, inertia, drag coefficient and radius;

Add a motor;

Add, if desired, aerodynamic surfaces;

Add, if desired, parachutes;

Set, if desired, rail guides;

See results.
"""
#CREATE ROCKET
XENIA2 = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=r'./src/flight_sim/sample_drag.csv',
    power_on_drag=r'./src/flight_sim/sample_drag.csv',
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

#NEED TO ADD THE HYBRID TO THE SHITASS XENIA 2 ROCKET
XENIA2.add_motor(example_hybrid, position=-1.255)

#can add rail guides to the rocket to get a better idea of off the rail velocity and stability!!!
"""
rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)
"""

#CAN ADD AERO SURFACES TO ROCKET
nose_cone = XENIA2.add_nose(
    length=0.55829, kind="von karman", position=1.278
)

fin_set = XENIA2.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=(r'./src/flight_sim/NACA0012-radians.csv',"radians"),
)

tail = XENIA2.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

#CAN ADD PARACHUTES!!!!!
main = XENIA2.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,      # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = XENIA2.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

####SUGGESTED TO PLOT STATIC MARGIN TO SEE STABILITY. SIM WILL FAIL IF OVERSTABLE OR NEGATIVE
XENIA2.plots.static_margin()


####LASTLY TO RUN SIM WE NEED TO CREATE A FLIGHT OBJECT
test_flight = Flight(
    rocket=XENIA2, environment=env, rail_length=5.2, inclination=85, heading=0
    )

test_flight.all_info() #BIG DATA