import request from './request.js'

export const reqAnalyze = ({ featureName, values }) => request({
    url: '/analyze',
    method: 'get',
    params: {
        features: featureName,
        ...values
    }
})