from pyasn1.debug import scope

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
class InstructorPortal(CustomerPortal):
    _items_per_page = 3

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user_id = request.env.user.id
        values['portal_instructor_courses'] = request.env['sms_module.course'].sudo().search_count([('teacher_id', '=', user_id)])
        return values

    @http.route(['/instructor_courses','/instructor_courses/page/<int:page>'], type='http', auth="user", website=True)
    def portal_instructor_courses(self, search=None , search_in='All' , sortby='name_asc' , filterby='All', page=1, groupby='none', **kwargs):
        searchbar_inputs = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Course Name': {'label': 'Course Name', 'input': 'Course Name',
                            'domain': [('name', 'ilike', search)]},
            'Course Level': {'label': 'Course Level', 'input': 'Course Level',
                             'domain': [('course_level', '=', search)]},
            'Course Duration': {'label': 'Course Duration', 'input': 'Course Duration',
                                'domain': [('duration', '=', search)]},
        }
        searchbar_sortings = {
            'name_asc': {'label': 'Course Name (A-Z)', 'order': 'name'},
            'name_desc': {'label': 'Course Name (Z-A)', 'order': 'name desc'},
            'course_duration_asc': {'label': 'Course Duration (Low to high)', 'order': 'course_duration'},
            'course_duration_desc': {'label': 'Course Duration (high to low)', 'order': 'course_duration desc'},
            'course_level_asc': {'label': 'Course Level (low to high)', 'order': 'course_level'},
            'course_level_desc': {'label': 'Course Level (high to low)', 'order': 'course_level desc'},
        }
        searchbar_filters = {
            'All': {'label': 'All', 'domain': []},
            'Featured': {'label': 'Featured', 'domain': [('is_featured', '=', True)]},
        }
        searchbar_groupby={
            'none': {'label': 'None', 'sequence': 10},
            'course_level': {'label': 'Course Level', 'sequence': 20},
            'duration': {'label': 'Course Duration', 'sequence': 30},
        }

        order = searchbar_sortings[sortby]['order']
        search_domain = searchbar_inputs[search_in]['domain']
        filter_domain = searchbar_filters.get(filterby, searchbar_filters['All'])['domain']
        combined_domain = [('teacher_id', '=', request.env.user.id)] + search_domain + filter_domain

        grouped = groupby and groupby != 'none'
        print(groupby)

        if grouped and groupby in searchbar_groupby:
            all_groups = request.env['sms_module.course'].sudo().read_group(
                domain=combined_domain,
                fields=[groupby],
                groupby=[groupby],
                orderby=order if groupby == 'teacher_id' else False
            )

            print("all_groups are", all_groups)


            if groupby != 'teacher_id':  # If not Many2one, sort manually
                reverse = 'desc' in order
                all_groups = sorted(all_groups, key=lambda c: c.get(groupby, 0), reverse=reverse)

            # **Step 2: Implement pagination on groups**
            total_groups = len(all_groups)  # Total number of groups
            pager = portal_pager(
                url="/instructor_courses",
                url_args={'search': search, 'search_in': search_in, 'sortby': sortby, 'filterby': filterby,
                          'groupby': groupby},
                total=total_groups,
                page=page,
                step=self._items_per_page,
                scope=100
            )

            # Get only the groups for the current page
            paged_groups = all_groups[pager['offset']:pager['offset'] + self._items_per_page]

            # **Step 3: Fetch full record lists per group**
            courses = []
            for group in paged_groups:
                group_data = {
                    'groupby': group[groupby],
                    'records': request.env['sms_module.course'].sudo().search(group['__domain'], order=order)
                }
                courses.append(group_data)
                print(courses)

        else:
            # Normal pagination for ungrouped data
            total_courses = request.env['sms_module.course'].sudo().search_count(combined_domain)
            pager = portal_pager(
                url="/instructor_courses",
                url_args={'search': search, 'search_in': search_in, 'sortby': sortby, 'filterby': filterby},
                total=total_courses,
                page=page,
                step=self._items_per_page,
            )
            courses = request.env['sms_module.course'].sudo().search(combined_domain, offset=pager['offset'],
                                                                     limit=self._items_per_page, order=order)
        print(groupby, grouped)

        return request.render('sms_module.portal_my_home_menu_instructor_course_view', {
            'courses': courses,
            'page_name':'instructor_courses',
            'pager': pager,
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'filterby': filterby,
            'searchbar_filters': searchbar_filters,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'grouped': grouped,
            'groupby': groupby,
            'searchbar_groupby': searchbar_groupby,
            'default_url': '/instructor_courses',

        })

    @http.route(['/instructor_courses/details/', '/instructor_courses/details/<int:course_id>'], type='http',
                auth="user", website=True)
    def portal_instructor_course_form(self, course_id=None, **kwargs):


        course = request.env['sms_module.course'].sudo().search(
            [('id', '=', course_id), ('teacher_id', '=',  request.env.user.id)], limit=1
        )

        instructor_courses = request.env['sms_module.course'].sudo().search(
            [('teacher_id', '=',  request.env.user.id)], order="id"
        )

        instructor_courses_ids = instructor_courses.ids
        current_index = instructor_courses_ids.index(course_id)

        if current_index != 0 and instructor_courses_ids[current_index - 1]:
            prev_record = f'/instructor_courses/details/{instructor_courses_ids[current_index - 1]}'
        else:
            prev_record = None

        if current_index != len(instructor_courses_ids) - 1 and instructor_courses_ids[current_index + 1]:
            next_record = f'/instructor_courses/details/{instructor_courses_ids[current_index + 1]}'
        else:
            next_record = None

        return request.render('sms_module.portal_instructor_course_details', qcontext={
            'course': course,
            'page_name': 'instructor_courses',
            'default_url': '/instructor_courses',
            'prev_record': prev_record,
            'next_record': next_record,

        })

    @http.route(['/instructor_courses/details/', '/instructor_courses/details/<int:course_id>'], type='http',
                auth="user", website=True)
    def portal_instructor_course_form(self, course_id=None, **kwargs):

        course = request.env['sms_module.course'].sudo().search(
            [('id', '=', course_id), ('teacher_id', '=', request.env.user.id)], limit=1
        )

        instructor_courses = request.env['sms_module.course'].sudo().search(
            [('teacher_id', '=', request.env.user.id)], order="id"
        )

        instructor_courses_ids = instructor_courses.ids
        current_index = instructor_courses_ids.index(course_id)

        if current_index != 0 and instructor_courses_ids[current_index - 1]:
            prev_record = f'/instructor_courses/details/{instructor_courses_ids[current_index - 1]}'
        else:
            prev_record = None

        if current_index != len(instructor_courses_ids) - 1 and instructor_courses_ids[current_index + 1]:
            next_record = f'/instructor_courses/details/{instructor_courses_ids[current_index + 1]}'
        else:
            next_record = None

        return request.render('sms_module.portal_instructor_course_details', qcontext={
            'course': course,
            'page_name': 'instructor_courses',
            'default_url': '/instructor_courses',
            'prev_record': prev_record,
            'next_record': next_record,

            'object': course,
            'disable_composer': True,
            'two_columns': True

        })

