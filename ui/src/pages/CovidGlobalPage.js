import React from 'react'

import { useLocation } from 'react-router'
import queryString from 'query-string'

import ErrorBoundary from '../components/ErrorBoundary'
import GlobalGraphContainer from '../containers/GlobalGraphContainer'
import MainLayout from '../layouts/MainLayout'


export const CovidGlobalPage = () => {
    
    const { search } = useLocation()

    const validGraphs = ['Confirmed', 'Deaths', 'Recovered', 'Mortality', 'Recovery']

    let query = queryString.parse(search.indexOf('?') === 0 ? search.substr(1) : search)

    let region = query.region ? Array.isArray(query.region) ? query.region : [query.region] : undefined
    let graph = validGraphs.indexOf(query.graph) !== -1 ? query.graph : undefined
    let showLog = query.showLog === 'true' ? true : false

    return (
        <MainLayout>
            <ErrorBoundary>
                <GlobalGraphContainer region={region} graph={graph} showLogParam={showLog} />
            </ErrorBoundary>
        </MainLayout>
    )
}

export default CovidGlobalPage