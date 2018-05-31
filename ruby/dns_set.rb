require 'net/netconf'
require 'net/netconf/jnpr'

login = { :target => '10.254.0.41', :username => 'lab',  :password => 'lab123', }

dns_config = "
  <configuration>
    <system>
      <name-server delete='delete'/>
      <name-server>
        <name>10.1.1.100</name>
      </name-server>
      <name-server>
        <name>10.1.1.200</name>
      </name-server>
    </system>
  </configuration>"

Netconf::SSH.new( login ) do |dev|
  dev.rpc.lock_configuration
  dev.rpc.load_configuration(dns_config) # , action: 'replace')
  dev.rpc.commit_configuration
  dev.rpc.unlock_configuration
end
