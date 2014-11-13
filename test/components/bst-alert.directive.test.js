/**
 * Copyright 2014 Red Hat, Inc.
 *
 * This software is licensed to you under the GNU General Public
 * License as published by the Free Software Foundation; either version
 * 2 of the License (GPLv2) or (at your option) any later version.
 * There is NO WARRANTY for this software, express or implied,
 * including the implied warranties of MERCHANTABILITY,
 * NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
 * have received a copy of GPLv2 along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 */

describe('Directive: bstAlert', function() {
    var scope,
        compile,
        element,
        elementScope;

    beforeEach(module('Bastion.components', 'components/views/bst-alert.html'));

    beforeEach(inject(function(_$compile_, _$rootScope_) {
        compile = _$compile_;
        scope = _$rootScope_;
    }));

    beforeEach(function() {
        element = angular.element('<div bst-alert ' +
            'success-messages="successMessages" ' +
            'info-messages="infoMessages" ' +
            'warning-messages="warningMessages" ' +
            'error-messages="errorMessages"></div>');

        scope.successMessages = [];
        scope.infoMessages = [];
        scope.warningMessages = [];
        scope.errorMessages = [];

        compile(element)(scope);
        scope.$digest();

        elementScope = element.isolateScope();
    });

    it("should display success alerts", function() {
        scope.successMessages = ['hello'];
        scope.$digest();

        expect(elementScope.alerts['success'].length).toBe(1);
        expect(elementScope.alerts['success'][0]).toBe('hello');
    });

    it("should display info alerts", function() {
        scope.infoMessages = ['hello'];
        scope.$digest();

        expect(elementScope.alerts['info'].length).toBe(1);
        expect(elementScope.alerts['info'][0]).toBe('hello');
    });

    it("should display warning alerts", function() {
        scope.warningMessages = ['hello'];
        scope.$digest();

        expect(elementScope.alerts['warning'].length).toBe(1);
        expect(elementScope.alerts['warning'][0]).toBe('hello');
    });

    it("should display success alerts", function() {
        scope.errorMessages = ['hello'];
        scope.$digest();

        expect(elementScope.alerts['danger'].length).toBe(1);
        expect(elementScope.alerts['danger'][0]).toBe('hello');
    });

    it("provides a way to close alerts", function() {
        elementScope.alerts = {success: ['yo!', 'hello'], danger: ['foo']};
        elementScope.closeAlert('success', 1);
        expect(elementScope.alerts['success'].length).toBe(1);
        expect(elementScope.alerts['danger'].length).toBe(1);
    });

});
