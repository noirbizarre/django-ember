describe("django-ember.js", function(){

    describe('initialization', function(){
        it('should load Ember.js', function(){
            expect(Ember).toBeDefined();
        });

        it('should load Ember-data', function(){
            expect(DS).toBeDefined();
        });

        it('should load Tastypie Adapter', function(){
            expect(DS.DjangoTastypieAdapter).toBeDefined();
        });

        it('should load Handlebars.js', function(){
            expect(Handlebars).toBeDefined();
        });
    });

});
