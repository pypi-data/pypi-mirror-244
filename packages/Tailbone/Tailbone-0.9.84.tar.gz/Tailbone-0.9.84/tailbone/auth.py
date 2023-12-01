# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Authentication & Authorization
"""

import logging
import re

from rattail import enum
from rattail.util import prettify, NOTSET

from zope.interface import implementer
from pyramid.interfaces import IAuthorizationPolicy
from pyramid.security import remember, forget, Everyone, Authenticated
from pyramid.authentication import SessionAuthenticationPolicy

from tailbone.db import Session


log = logging.getLogger(__name__)


def login_user(request, user, timeout=NOTSET):
    """
    Perform the steps necessary to login the given user.  Note that this
    returns a ``headers`` dict which you should pass to the redirect.
    """
    user.record_event(enum.USER_EVENT_LOGIN)
    headers = remember(request, user.uuid)
    if timeout is NOTSET:
        timeout = session_timeout_for_user(user)
    log.debug("setting session timeout for '{}' to {}".format(user.username, timeout))
    set_session_timeout(request, timeout)
    return headers


def logout_user(request):
    """
    Perform the logout action for the given request.  Note that this returns a
    ``headers`` dict which you should pass to the redirect.
    """
    user = request.user
    if user:
        user.record_event(enum.USER_EVENT_LOGOUT)
    request.session.delete()
    request.session.invalidate()
    headers = forget(request)
    return headers


def session_timeout_for_user(user):
    """
    Returns the "max" session timeout for the user, according to roles
    """
    from rattail.db.auth import authenticated_role

    roles = user.roles + [authenticated_role(Session())]
    timeouts = [role.session_timeout for role in roles
                if role.session_timeout is not None]
    if timeouts and 0 not in timeouts:
        return max(timeouts)


def set_session_timeout(request, timeout):
    """
    Set the server-side session timeout to the given value.
    """
    request.session['_timeout'] = timeout or None


class TailboneAuthenticationPolicy(SessionAuthenticationPolicy):
    """
    Custom authentication policy for Tailbone.

    This is mostly Pyramid's built-in session-based policy, but adds
    logic to accept Rattail User API Tokens in lieu of current user
    being identified via the session.

    Note that the traditional Tailbone web app does *not* use this
    policy, only the Tailbone web API uses it by default.
    """

    def unauthenticated_userid(self, request):

        # figure out userid from header token if present
        credentials = request.headers.get('Authorization')
        if credentials:
            match = re.match(r'^Bearer (\S+)$', credentials)
            if match:
                token = match.group(1)
                rattail_config = request.registry.settings.get('rattail_config')
                app = rattail_config.get_app()
                auth = app.get_auth_handler()
                user = auth.authenticate_user_token(Session(), token)
                if user:
                    return user.uuid

        # otherwise do normal session-based logic
        return super(TailboneAuthenticationPolicy, self).unauthenticated_userid(request)


@implementer(IAuthorizationPolicy)
class TailboneAuthorizationPolicy(object):

    def permits(self, context, principals, permission):
        config = context.request.rattail_config
        model = config.get_model()
        app = config.get_app()
        auth = app.get_auth_handler()

        for userid in principals:
            if userid not in (Everyone, Authenticated):
                if context.request.user and context.request.user.uuid == userid:
                    return context.request.has_perm(permission)
                else:
                    # this is pretty rare, but can happen in dev after
                    # re-creating the database, which means new user uuids.
                    # TODO: the odds of this query returning a user in that
                    # case, are probably nil, and we should just skip this bit?
                    user = Session.get(model.User, userid)
                    if user:
                        if auth.has_permission(Session(), user, permission):
                            return True
        if Everyone in principals:
            return auth.has_permission(Session(), None, permission)
        return False

    def principals_allowed_by_permission(self, context, permission):
        raise NotImplementedError


def add_permission_group(config, key, label=None, overwrite=True):
    """
    Add a permission group to the app configuration.
    """
    def action():
        perms = config.get_settings().get('tailbone_permissions', {})
        if key not in perms or overwrite:
            group = perms.setdefault(key, {'key': key})
            group['label'] = label or prettify(key)
        config.add_settings({'tailbone_permissions': perms})
    config.action(None, action)


def add_permission(config, groupkey, key, label=None):
    """
    Add a permission to the app configuration.
    """
    def action():
        perms = config.get_settings().get('tailbone_permissions', {})
        group = perms.setdefault(groupkey, {'key': groupkey})
        group.setdefault('label', prettify(groupkey))
        perm = group.setdefault('perms', {}).setdefault(key, {'key': key})
        perm['label'] = label or prettify(key)
        config.add_settings({'tailbone_permissions': perms})
    config.action(None, action)
