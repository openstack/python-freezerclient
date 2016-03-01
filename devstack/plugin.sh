# (c) Copyright 2014-2016 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# check for service enabled
if is_service_enabled python-freezerclient; then
    if [[ "$1" == "source" || "`type -t install_freezerclient`" != 'function' ]]; then
        # Initial source
        source $FREEZER_DIR/devstack/lib/python-freezerclient
    fi

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing python-freezerclient"
        install_freezerclient
    fi
fi

