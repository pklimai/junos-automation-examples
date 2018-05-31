require 'net/netconf'

login = { :target => '10.254.0.41', :username => 'lab',  :password => 'lab123', }

Netconf::SSH.new( login ) do |dev|
  full_config = dev.rpc.get_configuration
  full_config.xpath('system/name-server/name').each do |ip|
    puts ip.text
  end
end
