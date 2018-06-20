# -*- coding: utf-8 -*-

from .base import Service, VENDOR_MICROSOFT
from lapdance.exceptions import LapdanceError
from lapdance.models import LDAPGroup


class GroupService(Service):
    __model__ = LDAPGroup
    __config_name__ = 'LAPDANCE_LDAP_GROUP'

    @property
    def _users(self):
        """Imports and returns users service"""

        from lapdance.services import users
        return users

    def get_members(self, group_id, include_nested=False, **kwargs):
        group_dn = self.get_one(group_id).dn

        if include_nested in [str(1), 'true']:
            self._raise_if_incompatible_with(VENDOR_MICROSOFT)
            # @TODO - create something similar for non-AD
            nested_filter = '(memberOf:1.2.840.113556.1.4.1941:={0})'.format(group_dn)
        else:
            nested_filter = '(memberOf={0})'.format(group_dn)

        return self._users.get_many(nested_filter, **kwargs)

    def add_member(self, group_id, payload):
        user = self._users.get_one(payload['id'])
        group = self.get_one(group_id)
        if self._users.is_member_of(user.id, group.dn):
            msg = "User {0} is already member of {1}".format(user.id, group_id)
            raise LapdanceError(msg, status_code=400)

        # @TODO - create something similar for non-AD
        self._microsoft_ext.add_members_to_groups([user.dn], [group.dn], payload.pop('fix', False))

    def remove_member(self, group_id, user_id):
        user = self._users.get_one(user_id)
        group = self.get_one(group_id)
        if not self._users.is_member_of(user_id, group.dn):
            msg = "User {0} is not a member of {1}".format(user_id, group_id)
            raise LapdanceError(msg, status_code=400)

        # @TODO - create something similar for non-AD
        self._microsoft_ext.remove_members_from_groups([user.dn], [group.dn], fix=False)