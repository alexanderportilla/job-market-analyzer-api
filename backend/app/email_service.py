import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List, Dict
import json

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        
    def send_job_alert(self, user_email: str, user_name: str, matching_jobs: List[Dict], alert_keywords: List[str]):
        """Send job alert email to user"""
        subject = f"🚀 Nuevas ofertas de trabajo para: {', '.join(alert_keywords)}"
        
        # Create HTML content
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                .job-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #2563eb; }}
                .company {{ color: #666; font-size: 14px; }}
                .location {{ color: #888; font-size: 12px; }}
                .description {{ margin: 10px 0; }}
                .button {{ background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Job Market Analyzer</h1>
                <p>Nuevas ofertas de trabajo encontradas</p>
            </div>
            
            <div style="padding: 20px;">
                <h2>Hola {user_name},</h2>
                <p>Hemos encontrado <strong>{len(matching_jobs)}</strong> nuevas ofertas de trabajo que coinciden con tus criterios:</p>
                <p><strong>Palabras clave:</strong> {', '.join(alert_keywords)}</p>
                
                <h3>📋 Ofertas Encontradas:</h3>
        """
        
        for job in matching_jobs:
            html_content += f"""
                <div class="job-card">
                    <div class="job-title">{job['title']}</div>
                    <div class="company">🏢 {job['company']}</div>
                    <div class="location">📍 {job['location']}</div>
                    <div class="description">{job['description'][:200]}...</div>
                    <a href="{job['url']}" class="button" target="_blank">Ver Oferta</a>
                </div>
            """
        
        html_content += f"""
            </div>
            
            <div class="footer">
                <p>Este email fue enviado por Job Market Analyzer</p>
                <p>Para desactivar las alertas, visita tu perfil en la aplicación</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def send_welcome_email(self, user_email: str, user_name: str):
        """Send welcome email to new users"""
        subject = "🎉 ¡Bienvenido a Job Market Analyzer!"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Job Market Analyzer</h1>
            </div>
            
            <div class="content">
                <h2>¡Hola {user_name}!</h2>
                <p>¡Bienvenido a Job Market Analyzer! Tu plataforma para analizar el mercado laboral tech en Colombia.</p>
                
                <h3>🚀 ¿Qué puedes hacer?</h3>
                <ul>
                    <li>📊 Ver estadísticas del mercado en tiempo real</li>
                    <li>🔍 Buscar ofertas de trabajo con filtros avanzados</li>
                    <li>📈 Analizar tendencias de tecnologías</li>
                    <li>🔔 Configurar alertas personalizadas</li>
                    <li>💾 Guardar ofertas favoritas</li>
                </ul>
                
                <p><a href="http://localhost:3000" class="button">Comenzar a Explorar</a></p>
                
                <p>¡Gracias por unirte a nuestra comunidad!</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def send_market_insights(self, user_email: str, user_name: str, insights: Dict):
        """Send weekly market insights email"""
        subject = "📈 Insights Semanales del Mercado Laboral Tech"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                .insight-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Market Insights</h1>
                <p>Resumen semanal del mercado laboral tech</p>
            </div>
            
            <div style="padding: 20px;">
                <h2>Hola {user_name},</h2>
                <p>Aquí tienes tu resumen semanal del mercado laboral tech en Colombia:</p>
                
                <div class="insight-card">
                    <h3>📈 Crecimiento del Mercado</h3>
                    <p>Ofertas nuevas esta semana: <strong>{insights.get('new_offers', 0)}</strong></p>
                    <p>Tasa de crecimiento: <strong>{insights.get('growth_rate', 0)}%</strong></p>
                </div>
                
                <div class="insight-card">
                    <h3>🔥 Tecnologías en Tendencia</h3>
                    <ul>
                        {''.join([f'<li>{tech}</li>' for tech in insights.get('trending_techs', [])])}
                    </ul>
                </div>
                
                <div class="insight-card">
                    <h3>💡 Recomendaciones</h3>
                    <ul>
                        {''.join([f'<li>{rec}</li>' for rec in insights.get('recommendations', [])])}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def _send_email(self, to_email: str, subject: str, html_content: str):
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False 