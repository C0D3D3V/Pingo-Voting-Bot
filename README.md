# Pingo Voting Bot
This is only a proof of concept.

This is a voting bot for the voting system of the University of Paderborn. 
You can reach the page with this link: http://pingo.upb.de/


The `pingoVoter.py` script votes x times for every option on a pingo survey.
  
Set the following in the file `config.ini` before running the script

- `url` : URL for pingo survey
- `loglevel` : Sets the level of logging (0 - less information / 5 - all information)


#### REQUIREMENTS

- Python 2.7+
- Beautifulsoup - `sudo apt-get install python-beautifulsoup`
- Colorama - `sudo pip install colorama`
- Termcolor - `sudo pip install termcolor`


Copyright 2017 Daniel Vogt

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
