#-*- coding: UTF-8 -*-
from Products.CMFPlone import PloneMessageFactory as _p
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from Products.CMFPlone.utils import log
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
import logging

class ReviewViewlet(WorkflowHistoryViewlet):
    render = ViewPageTemplateFile("templates/review_history.pt")
    
    def workflowHistory(self, complete=True):
        """Return workflow history of this context.

        Taken from plone_scripts/getWorkflowHistory.py
        """
        context = aq_inner(self.context)
        # check if the current user has the proper permissions
#        if not (_checkPermission('Request review', context) or
#            _checkPermission('Review portal content', context)):
#            return []

        workflow = getToolByName(context, 'portal_workflow')
        membership = getToolByName(context, 'portal_membership')

        review_history = []

        try:
            # get total history
#            import pdb
#            pdb.set_trace()
            review_history = workflow.getInfoFor(context, 'review_history')

            if not complete:
                # filter out automatic transitions.
                review_history = [r for r in review_history if r['action']]
            else:
                review_history = list(review_history)

            portal_type = context.portal_type
            anon = _p(u'label_anonymous_user', default=u'Anonymous User')

            for r in review_history:
                r['type'] = 'workflow'
                r['transition_title'] = workflow.getTitleForTransitionOnType(
                    r['action'], portal_type) or _p("Create")
                r['state_title'] = workflow.getTitleForStateOnType(
                    r['review_state'], portal_type)
                actorid = r['actor']
                r['actorid'] = actorid
                if actorid is None:
                    # action performed by an anonymous user
                    r['actor'] = {'username': anon, 'fullname': anon}
                    r['actor_home'] = ''
                else:
                    r['actor'] = membership.getMemberInfo(actorid)
                    if r['actor'] is not None:
                        r['actor_home'] = self.navigation_root_url + '/author/' + actorid
                    else:
                        # member info is not available
                        # the user was probably deleted
                        r['actor_home'] = ''
            review_history.reverse()

        except WorkflowException:
            log('plone.app.layout.viewlets.content: '
                '%s has no associated workflow' % context.absolute_url(),
                severity=logging.DEBUG)

        return review_history
    