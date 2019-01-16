# Scrapper
	listar todos los PRs de un repo

	caracteristicas para que el PR sea sujeto de análisis:
	    que haya sido revisado y no mergeado directamente
		que el repo activity sea mayor que N
			* repo activity: media de latency de N PRs closed en N días previos
		diff menor que 2000 y mayor que 0

	análisis:
		obtener diff (string)
		obtener latency (open date - close date) (number)
		obtener repo activity (number)


# Neuronal network
	X: diff, repo_activity
	y: latency


DEA
    grafico temporal que muestre el valor de occurrences_nearest_coll (para mostrar que el pace no es uniforme)
    check for uotliers regarding mean latency
    perform analysis correlations

add renames