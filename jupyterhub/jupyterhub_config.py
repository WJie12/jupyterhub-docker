# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##
# GitLab Authenticator
#OAUTH_CALLBACK_URL='https://10.19.129.71/hub/oauth_callback'
#GITLAB_CLIENT_ID=0e26f98f758b334e3afc20b1c25f1263ac21f5b2919f4547d962bf459d590d42
#GITLAB_CLIENT_SECRET=c7d0d313d92dcee0352e24135e54e2d1c51f5b0158a1e1a6ad3dbd2720798bfc
GITLAB_HOST='10.19.129.71:9829'

import os

## Configure authentication (delagated to Gitlab)
from oauthenticator.gitlab import GitLabOAuthenticator
c.JupyterHub.authenticator_class = GitLabOAuthenticator

c.GitLabOAuthenticator.oauth_callback_url = 'https://10.19.129.71/hub/oauth_callback'
c.GitLabOAuthenticator.client_id = '493c60b178c6dcd2597c78ff82fb08dff366d9cbc5c6ca875b55601fcc6e9694'
c.GitLabOAuthenticator.client_secret = '3db63e057b30e868a89c34841431bff94ff09475b8b0d0709b6bab6280df2767'
## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authenticator
#from jhub_cas_authenticator.cas_auth import CASAuthenticator
#c.JupyterHub.authenticator_class = CASAuthenticator

# The CAS URLs to redirect (un)authenticated users to.
#c.CASAuthenticator.cas_login_url = 'https://cas.uvsq.fr/login'
#c.CASLocalAuthenticator.cas_logout_url = 'https://cas.uvsq/logout'

# The CAS endpoint for validating service tickets.
#c.CASAuthenticator.cas_service_validate_url = 'https://cas.uvsq.fr/serviceValidate'

# The service URL the CAS server will redirect the browser back to on successful authentication.

#c.CASAuthenticator.cas_service_url = 'https://%s/hub/login' % os.environ['HOST']

#c.Authenticator.admin_users = { 'lucadefe' }


## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/zlab/data/jupyterhub'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
