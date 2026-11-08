import axios from "axios";
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||"http://localhost:8000/api/v1",timeout:20000});
api.interceptors.request.use(config=>{const token=localStorage.getItem("clinassist_token");if(token)config.headers.Authorization=`Bearer ${token}`;return config});
export type ModelName="logistic_regression"|"random_forest"|"xgboost";
export type Features={Pregnancies:number;Glucose:number;BloodPressure:number;SkinThickness:number;Insulin:number;BMI:number;DiabetesPedigreeFunction:number;Age:number};
export type Prediction={model_version:string;data_source_note:string;probability:number;risk_category:string;prediction:number;abstain:boolean;uncertainty:number|null;confidence_statement:string;feature_contributions:{feature:string;value:number;contribution:number;direction:string;method?:string}[]|null;limitations:string[];clinical_disclaimer:string};
export async function predict(features:Features,modelName:ModelName="logistic_regression"){
    return (await api.post<Prediction>("/predict",{features,model_name:modelName,return_explanation:true,return_uncertainty:true})).data;
}
