docker-compose down
docker-compose up --build

Étape 6 : Vérifier les logs
Vérifiez les logs de Celery Beat pour voir si les tâches sont planifiées correctement :
-docker-compose logs celery-beat
Vérifiez les logs du worker Celery pour voir si les tâches sont exécutées :
-docker-compose logs celery-worker
