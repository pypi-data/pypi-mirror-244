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
CORE POS "lane" views
"""

from rattail_corepos.corepos.office.util import get_fannie_config_value

from .master import CoreOfficeMasterView


class LaneView(CoreOfficeMasterView):
    """
    Master view for CORE lanes
    """
    model_key = 'number'
    model_title = "CORE-POS Lane"
    url_prefix = '/core-pos/lanes'
    route_prefix = 'corepos.lanes'
    filterable = False
    pageable = False
    creatable = False
    viewable = False
    editable = False
    deletable = False
    results_downloadable = False

    grid_columns = [
        'number',
        'host',
        'type',
        'op',
        'trans',
        'offline',
    ]

    def get_data(self, session=None):
        data = []
        lanes = get_fannie_config_value(self.rattail_config, 'LANES')

        for i, lane in enumerate(lanes, 1):
            lane_data = dict(lane)
            lane_data['number'] = i
            del lane_data['user']
            del lane_data['pw']
            data.append(lane_data)

        return data


def defaults(config, **kwargs):
    base = globals()

    LaneView = kwargs.get('LaneView', base['LaneView'])
    LaneView.defaults(config)


def includeme(config):
    defaults(config)
