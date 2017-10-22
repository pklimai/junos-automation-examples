#!/usr/bin/ruby

class Vehicle
  
  @@totalVehicles = 0
  
  # class method
  def self.totalVehicles
    @@totalVehicles
  end

  def initialize(type, make, model)
    @type = type
    @make = make
    @model = model
    @@totalVehicles += 1
  end
 
  def to_s()
    "Vehicle type: #{@type} Make: #{@make} Model: #{@model}"
  end
end

mers = Vehicle.new("Car", "Mersedes", "S600")
kamaz = Vehicle.new("Truck", "KAMAZ", "K1")
ferrari = Vehicle.new("F1 Bolid", "Ferrari", "none")

puts mers, kamaz, ferrari
puts "Total cars: #{Vehicle.totalVehicles}"
