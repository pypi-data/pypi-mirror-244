#   Flask-Allow allows white/black listing of ip addresses/networks.
#   Copyright (C) 2023 Marc Bertens-Nguyen
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; only version 2
#   of the License (GPL-2.0-only).
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
__version__ = '2.0.0'
__author__  = 'Marc Bertens-Nguyen'
__licence__ = 'GPL-2.0-only'


class InvalidAccessLog( Exception ):
    def __init__( self, message, data ):
        super().__init__( message )
        self.data = data
        return
