import openai
import os
from typing import List, Dict, Optional
import json

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("⚠️ OPENAI_API_KEY not found. AI features will be disabled.")
    
    def analyze_job_description(self, job_description: str, job_title: str) -> Dict:
        """Analyze job description using ChatGPT"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            prompt = f"""
            Analiza la siguiente descripción de trabajo y proporciona insights detallados:
            
            Título: {job_title}
            Descripción: {job_description}
            
            Por favor proporciona:
            1. Tecnologías mencionadas
            2. Nivel de experiencia requerido
            3. Responsabilidades principales
            4. Requisitos técnicos
            5. Salario estimado (en pesos colombianos)
            6. Beneficios mencionados
            7. Tipo de contrato (si se menciona)
            8. Ubicación de trabajo (remoto/presencial/híbrido)
            
            Responde en formato JSON.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto analista de ofertas de trabajo tech. Proporciona análisis detallados y precisos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            return json.loads(analysis)
            
        except Exception as e:
            return {"error": f"Error analyzing job: {str(e)}"}
    
    def generate_market_insights(self, job_data: List[Dict]) -> Dict:
        """Generate market insights from job data"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            # Prepare job data for analysis
            job_summary = []
            for job in job_data[:20]:  # Limit to first 20 jobs
                job_summary.append({
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "description": job.get("description", "")[:200]  # Truncate for token limit
                })
            
            prompt = f"""
            Analiza los siguientes datos de ofertas de trabajo tech en Colombia y proporciona insights del mercado:
            
            Datos de ofertas: {json.dumps(job_summary, ensure_ascii=False)}
            
            Por favor proporciona:
            1. Tendencias principales del mercado
            2. Tecnologías más demandadas
            3. Niveles de experiencia más solicitados
            4. Ubicaciones con más oportunidades
            5. Empresas más activas en contratación
            6. Recomendaciones para candidatos
            7. Predicciones del mercado para los próximos meses
            
            Responde en formato JSON con las siguientes claves:
            - trends
            - top_technologies
            - experience_levels
            - top_locations
            - active_companies
            - recommendations
            - predictions
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto analista del mercado laboral tech en Colombia. Proporciona insights valiosos y predicciones basadas en datos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.4
            )
            
            insights = response.choices[0].message.content
            return json.loads(insights)
            
        except Exception as e:
            return {"error": f"Error generating insights: {str(e)}"}
    
    def generate_job_recommendations(self, user_profile: Dict, available_jobs: List[Dict]) -> List[Dict]:
        """Generate personalized job recommendations"""
        if not self.api_key:
            return [{"error": "OpenAI API key not configured"}]
        
        try:
            prompt = f"""
            Basándote en el perfil del usuario y las ofertas disponibles, genera recomendaciones personalizadas:
            
            Perfil del usuario:
            - Experiencia: {user_profile.get('experience', 'N/A')}
            - Tecnologías: {user_profile.get('technologies', [])}
            - Ubicación preferida: {user_profile.get('location', 'N/A')}
            - Tipo de trabajo: {user_profile.get('job_type', 'N/A')}
            
            Ofertas disponibles: {json.dumps(available_jobs[:15], ensure_ascii=False)}
            
            Para cada oferta recomendada, proporciona:
            1. Score de compatibilidad (1-10)
            2. Razones de la recomendación
            3. Tecnologías que coinciden
            4. Sugerencias para la aplicación
            
            Responde en formato JSON con una lista de recomendaciones.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en matching de candidatos con ofertas de trabajo. Proporciona recomendaciones precisas y útiles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.3
            )
            
            recommendations = response.choices[0].message.content
            return json.loads(recommendations)
            
        except Exception as e:
            return [{"error": f"Error generating recommendations: {str(e)}"}]
    
    def generate_cv_analysis(self, cv_text: str, job_description: str) -> Dict:
        """Analyze CV against job description"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            prompt = f"""
            Analiza la compatibilidad entre el CV del candidato y la descripción del trabajo:
            
            CV del candidato:
            {cv_text}
            
            Descripción del trabajo:
            {job_description}
            
            Proporciona:
            1. Score de compatibilidad general (1-10)
            2. Fortalezas del candidato
            3. Áreas de mejora
            4. Tecnologías que coinciden
            5. Experiencia relevante
            6. Sugerencias para mejorar el CV
            7. Probabilidad de éxito en la aplicación
            
            Responde en formato JSON.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en recursos humanos y análisis de CVs. Proporciona análisis honestos y constructivos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            return json.loads(analysis)
            
        except Exception as e:
            return {"error": f"Error analyzing CV: {str(e)}"}
    
    def generate_interview_preparation(self, job_description: str, user_profile: Dict) -> Dict:
        """Generate interview preparation tips"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            prompt = f"""
            Genera una guía de preparación para entrevista basada en:
            
            Descripción del trabajo:
            {job_description}
            
            Perfil del candidato:
            {json.dumps(user_profile, ensure_ascii=False)}
            
            Proporciona:
            1. Preguntas técnicas probables
            2. Preguntas de comportamiento esperadas
            3. Puntos fuertes a destacar
            4. Áreas de mejora a abordar
            5. Preguntas para hacer al entrevistador
            6. Consejos específicos para el rol
            7. Recursos de estudio recomendados
            
            Responde en formato JSON.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en preparación de entrevistas tech. Proporciona consejos prácticos y específicos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.4
            )
            
            preparation = response.choices[0].message.content
            return json.loads(preparation)
            
        except Exception as e:
            return {"error": f"Error generating preparation: {str(e)}"} 