import re
import alc
from alc import radius

# Get the calling-station-id/username
csid = radius.attributes.get(1)

# Get the remote-id 
remoteid = radius.attributes.getVSA(3561, 2)

# Remove any extra characters from start of remote-id
dash_pos = remoteid.find('-')
if dash_pos > 5 :
 remoteid = remoteid[4:]

# Parse the csid into an array
key_list = ('node', 'tech', 'port', 'ont', 'gem', 'vlan')
csid_list = re.split(r'[. :]', csid)
csid_dict = dict(zip(key_list, csid_list))

# Check if user is xpon(FTTH)
if csid_dict.get('tech') == 'xpon':

 # Check if GEM port not 1
 if csid_dict.get('gem') != '1':

  # Set GEM port to 1
  csid_dict['gem'] = '1'

  # Rebuild the csid string with the new GEM port value
  csid = csid_dict['node'] + ' ' + \
  csid_dict['tech'] + ' ' + \
  csid_dict['port'] + ':' + \
  csid_dict['ont'] + '.' + \
  csid_dict['gem'] + '.' + \
  csid_dict['vlan']

  # Set the calling-station-id/username with the corrected GEM port value
  radius.attributes.set (1, csid)

  # Set calling-station-id, agent-remote-id 
  radius.attributes.setVSA (3561, 1, csid) 
  radius.attributes.setVSA (3561, 2, remoteid)

