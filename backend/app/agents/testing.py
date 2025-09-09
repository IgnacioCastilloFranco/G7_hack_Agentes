from app.agents.ratoncito_agent import create_ratoncito_agent

def test_ratoncito():
    """Test del Ratoncito con manejo robusto de errores"""
    print("🧪 === PRUEBA BÁSICA DEL RATONCITO PÉREZ ===\n")
    
    try:
        print("📝 Creando agente...")
        ratoncito = create_ratoncito_agent()
        print("✅ Agente creado exitosamente!\n")
        
        test_messages = [
            "¡Hola Ratoncito Pérez!",
            "Cuéntame sobre el Palacio Real",
            "¿Qué me puedes decir del Retiro?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"--- Prueba {i} ---")
            print(f"👤 Usuario: {message}\n")
            
            try:
                response = ratoncito.chat(message)
                
                if response.get("success", False):
                    print(f"🐭 Ratoncito: {response['response']}")
                else:
                    print(f"❌ Error: {response.get('error', 'Error desconocido')}")
                    # FAILSAFE DE EMERGENCIA
                    print(f"🆘 Respuesta alternativa: ¡Por mis bigotitos! Madrid es mágico. ¡Pregúntame más cosas! 🐭✨")
            
            except Exception as e:
                print(f"❌❌ Error crítico: {str(e)}")
                print(f"🆘 Respuesta de emergencia: ¡Por mis bigotitos! ¡Qué aventura tendremos hoy por Madrid! 🐭✨")
            
            print("\n" + "="*50 + "\n")
    
    except Exception as e:
        print(f"❌❌❌ Error fatal: {str(e)}")
        print("No se pudo inicializar el agente. Verifica la configuración.")

if __name__ == "__main__":
    test_ratoncito()



#***********PARA PROBAR CON EL AGENTE SIMPLE, COMENTAR LO DE ARRIBA Y DESCOMENTAR EL CÓDIGO DE ABAJO, Y EJECUTAR EL ARCHIVO: python -m app.agents.testing***************




# from app.agents.simple_ratoncito import create_magic_ratoncito_agent

# def test_ratoncito():
#     print("🧪 === PRUEBA DEL RATONCITO PÉREZ MÁGICO (SIN REACT) ===\n")
    
#     try:
#         print("📝 Creando agente mágico...")
#         ratoncito = create_magic_ratoncito_agent()
#         print("✅ Agente mágico creado exitosamente!\n")
        
#         test_messages = [
#             "¡Hola Ratoncito Pérez!",
#             "Cuéntame sobre el Palacio Real",
#             "¿Qué me puedes decir del Retiro?",
#             "¿Dónde vives exactamente?",
#             "¿Qué lugares de Madrid me recomiendas?",
#             "¿Cómo recoges los dientes?",
#             "Háblame del Museo del Prado"
#         ]
        
#         for i, message in enumerate(test_messages, 1):
#             print(f"--- Prueba {i} ---")
#             print(f"👤 Usuario: {message}")
#             print()
            
#             try:
#                 result = ratoncito.chat(message)
                
#                 if result["success"]:
#                     print(f"🐭 Ratoncito: {result['response']}")
#                     print(f"📊 Tipo: {result.get('type', 'unknown')} | Intención: {result.get('intent', 'unknown')}")
#                 else:
#                     print(f"❌ Error: {result.get('error', 'Error desconocido')}")
                    
#             except Exception as e:
#                 print(f"❌ Error: {str(e)}")
            
#             print("\n" + "="*50 + "\n")
            
#     except Exception as e:
#         print(f"❌ Error creando el agente: {str(e)}")

# if __name__ == "__main__":
#     test_ratoncito()