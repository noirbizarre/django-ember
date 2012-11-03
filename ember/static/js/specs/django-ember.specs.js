describe("django-ember.js", function(){

    describe('initialization', function(){
        it('should load django.js', function(){
            // Wait for Django.js initialization
            var callback = jasmine.createSpy();
            Django.onReady(callback);

            waitsFor(function() {
                return callback.callCount > 0;
            });

            runs(function() {
                expect(callback).toHaveBeenCalled();
                expect(Django).toBeDefined();
            });

        });

        it('should load ember.js', function(){
            expect(Ember).toBeDefined();
        });
    });

});
