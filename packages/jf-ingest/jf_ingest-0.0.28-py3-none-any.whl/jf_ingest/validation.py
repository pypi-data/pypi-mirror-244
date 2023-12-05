from jira import JIRA, JIRAError

from jf_ingest.jf_jira.auth import get_jira_connection, JiraAuthConfig, JiraAuthMethod
from jf_ingest.jf_jira import JiraIngestionConfig
from jf_ingest.jf_jira.downloaders import download_users, download_projects_and_versions
from jf_ingest.utils import retry_for_429s
from requests.exceptions import RequestException


def validate_jira(config: JiraIngestionConfig):
    """
    Validates jira configuration and credentials. Lift-and-shift from the agent repo (for now).
    """
    auth_config: JiraAuthConfig = config.auth_config

    print("\nJira details:")
    print(f"  URL:      {auth_config.url}")
    print(f"  Username: {auth_config.user}")
    if auth_config.user and auth_config.password:
        print("  Password: **********")
    elif auth_config.personal_access_token:
        print("  Token: **********")
    else:
        print("No Jira credentials found in Jira authentication config!")
        return False

    # test Jira connection
    try:
        print("==> Testing Jira connection...")
        jira_connection = get_jira_connection(
            config=auth_config, auth_method=JiraAuthMethod.BasicAuth, max_retries=1
        )
        jira_connection.myself()
    except JIRAError as e:
        print(e)

        print("Response:")
        print("  Headers:", e.headers)
        print("  URL:", e.url)
        print("  Status Code:", e.status_code)
        print("  Text:", e.text)

        if "Basic authentication with passwords is deprecated." in str(e):
            print(
                f"Error connecting to Jira instance at {auth_config.url}. Please use a Jira API token, see https://confluence.atlassian.com/cloud/api-tokens-938839638.html"
            )
        else:
            print(
                f"Error connecting to Jira instance at {auth_config.url}, please validate your credentials. Error: {e}"
            )
        return False
    except RequestException as e:
        print(e)

        # Print debugging information related to the request exception
        if e.request:
            print("Request:")
            print("  URL:", e.request.method, e.request.url)
            print("  Body:", e.request.body)
        else:
            print('RequestException contained no "request" value.')

        if e.response:
            print("Response:")
            print("  Headers:", e.response.headers)
            print("  URL:", e.response.url)
            print("  Status Code:", e.response.status_code)
            print("  Text:", e.response.text)
        else:
            print('RequestException contained no "response" value.')

        return False
    except Exception as e:
        raise

    # test jira users permission
    try:
        print("==> Testing Jira user browsing permissions...")
        user_count = len(
            download_users(
                jira_basic_connection=jira_connection,
                jira_atlas_connect_connection=None,
                gdpr_active=config.gdpr_active,
            )
        )
        print(f"The agent is aware of {user_count} Jira users.")

    except Exception as e:
        print(
            f'Error downloading users from Jira instance at {auth_config.url}, please verify that this user has the "browse all users" permission. Error: {e}'
        )
        return False

    # test jira project access
    print("==> Testing Jira project permissions...")
    accessible_projects = [p.key for p in retry_for_429s(jira_connection.projects)]
    print(f"The agent has access to projects {accessible_projects}.")

    inaccessible_projects = []

    if config.include_projects:
        for proj in config.include_projects:
            if proj not in accessible_projects:
                inaccessible_projects.append(proj)

    if inaccessible_projects:
        project_list_str = ", ".join(inaccessible_projects)
        print(
            f"\nERROR: Unable to access the following projects explicitly included in the config file! {project_list_str}."
        )
        return False
