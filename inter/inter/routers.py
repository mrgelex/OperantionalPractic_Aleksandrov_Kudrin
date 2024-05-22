class Dbrout():
    routeapp={'main'}
    def db_for_read(self, model):
        if model._meta.app_label in self.routeapp:
            return 'devices'
        return None
    
    # def allow_migrate(self, db, app_label, model_name=None):
    #     if app_label in self.routeapp:
    #         return db == 'devices'
    #     return None