#!/usr/bin/ruby

def process_interface(interface)
  if interface =~ /ge-.*/
    yield "#{interface} is gigabit"
  else
    yield "#{interface} is of unknown speed"
  end
end

interfaces = ["ge-1/0/5", "fxp0"]

interfaces.each do |intf| 
  process_interface(intf) { |str| puts str }
end

3.times { puts "---------" }
