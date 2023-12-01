# coding: utf-8

"""
    Hangar API

    This page describes the format for the current Hangar REST API as well as general usage guidelines.<br> Note that all routes **not** listed here should be considered **internal**, and can change at a moment's notice. **Do not use them**.  ## Authentication and Authorization There are two ways to consume the API: Authenticated or anonymous.  ### Anonymous When using anonymous authentication, you only have access to public information, but you don't need to worry about creating and storing an API key or handing JWTs.  ### Authenticated If you need access to non-public content or actions, you need to create and use API keys. These can be created by going to the API keys page via the profile dropdown or by going to your user page and clicking on the key icon.  API keys allow you to impersonate yourself, so they should be handled like passwords. **Do not share them with anyone else!**  #### Getting and Using a JWT Once you have an API key, you need to authenticate yourself: Send a `POST` request with your API key identifier to `/api/v1/authenticate?apiKey=yourKey`. The response will contain your JWT as well as an expiration time. Put this JWT into the `Authorization` header of every request and make sure to request a new JWT after the expiration time has passed.  Please also set a meaningful `User-Agent` header. This allows us to better identify loads and needs for potentially new endpoints.  ## Misc ### Date Formats Standard ISO types. Where possible, we use the [OpenAPI format modifier](https://swagger.io/docs/specification/data-models/data-types/#format).  ### Rate Limits and Caching The default rate limit is set at 20 requests every 5 seconds with an initial overdraft for extra leniency. Individual endpoints, such as version creation, may have stricter rate limiting.  If applicable, always cache responses. The Hangar API itself is cached by CloudFlare and internally.

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from hangar_api.models.project import Project

class TestProject(unittest.TestCase):
    """Project unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Project:
        """Test Project
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Project`
        """
        model = Project()
        if include_optional:
            return Project(
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                name = '',
                namespace = hangar_api.models.project_namespace.ProjectNamespace(
                    owner = '', 
                    slug = 'Maintenance', ),
                stats = hangar_api.models.project_stats.ProjectStats(
                    views = 56, 
                    downloads = 56, 
                    recent_views = 56, 
                    recent_downloads = 56, 
                    stars = 56, 
                    watchers = 56, ),
                category = 'admin_tools',
                last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                visibility = 'PUBLIC',
                avatar_url = '',
                description = '',
                user_actions = hangar_api.models.user_actions.UserActions(
                    starred = True, 
                    watching = True, 
                    flagged = True, ),
                settings = hangar_api.models.project_settings.ProjectSettings(
                    links = [
                        hangar_api.models.link_section.LinkSection(
                            id = 56, 
                            type = 'TOP', 
                            title = '', 
                            links = [
                                hangar_api.models.link.Link(
                                    id = 56, 
                                    name = '', 
                                    url = '', )
                                ], )
                        ], 
                    tags = [
                        ''
                        ], 
                    license = hangar_api.models.project_license.ProjectLicense(
                        name = '', 
                        url = '', 
                        type = '', ), 
                    keywords = [
                        ''
                        ], 
                    sponsors = '', 
                    donation = hangar_api.models.project_donation_settings.ProjectDonationSettings(
                        enable = True, 
                        subject = '', ), )
            )
        else:
            return Project(
        )
        """

    def testProject(self):
        """Test Project"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
