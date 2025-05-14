package furhatos.app.chat

import furhatos.flow.kotlin.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.voice.PollyNeuralVoice
import furhatos.flow.kotlin.voice.AcapelaVoice
import furhatos.util.Language
import java.net.InetSocketAddress
import com.sun.net.httpserver.HttpExchange
import com.sun.net.httpserver.HttpHandler
import com.sun.net.httpserver.HttpServer
import furhatos.gestures.Gestures
import org.json.JSONObject

class SimpleSkill : Skill() {
    override fun start() {
        Flow().run(Init)
    }
}

val Init: State = state {
    onEntry {
        // furhat.voice = PollyNeuralVoice(name="Adriano-Neural")
        // furhat.say("Ciao! Sono Furhat. Aspetto un messaggio esterno.")
        furhat.setInputLanguage(Language.ITALIAN) // Per la speech recognition

        // Usare Aurora o Alessio, che includono tutti i suoni #...#
        furhat.voice = AcapelaVoice(name="Vittorio22k_HQ")
        // furhat.voice = AcapelaVoice(name="Alessio22k_HQ")
        // furhat.voice = AcapelaVoice(name="Aurora22k_HQ")

        startServer() // Avvia il server HTTP
    }
}

fun startServer() {
    val server = HttpServer.create(InetSocketAddress(8081), 0)
    server.createContext("/speak", SpeakHandler())
    server.createContext("/fetch_speech", FetchSpeechHandler())
    server.executor = null
    server.start()
    println("Server avviato sulla porta 8081")
}

class SpeakHandler : HttpHandler {
    override fun handle(exchange: HttpExchange) {
        if (exchange.requestMethod == "POST") {
            // Legge il corpo della richiesta
            val requestBody = exchange.requestBody.bufferedReader().use { it.readText() }
            val json = JSONObject(requestBody)

            // Estrai i dati dal JSON
            val message = json.getString("text")  // Messaggio da pronunciare
            val age = json.optInt("age", -1)  // Età dell'utente (default -1 se non fornita)

            println("Messaggio ricevuto: $message")
            println("Età utente: ${if (age != -1) age else "Non specificata"}")

            // Processa il messaggio (puoi aggiungere logica per personalizzarlo in base all'età)
            Flow().runAsync(processMessage(exchange, message, age))
        } else {
            exchange.sendResponseHeaders(405, -1)
        }
    }
}

val processMessage: (HttpExchange, String, Int) -> State = { exchange, message, age ->
    state {
        onEntry {
            if(age < 13) {
                furhat.voice = AcapelaVoice(name="Alessio22k_HQ")
                furhat.setMask("child")
            } else {
                furhat.voice = AcapelaVoice(name="Vittorio22k_HQ")
                furhat.setMask("adult")
            }

            val gesturePattern = "<([A-Za-z]+)>".toRegex()
            val gestureMap = mapOf(
                "BigSmile" to Gestures.BigSmile,
                "Blink" to Gestures.Blink,
                "BrowFrown" to Gestures.BrowFrown,
                "BrowRaise" to Gestures.BrowRaise,
                "CloseEyes" to Gestures.CloseEyes,
                "ExpressAnger" to Gestures.ExpressAnger,
                "ExpressDisgust" to Gestures.ExpressDisgust,
                "ExpressFear" to Gestures.ExpressFear,
                "ExpressSad" to Gestures.ExpressSad,
                "GazeAway" to Gestures.GazeAway,
                "Nod" to Gestures.Nod,
                "Oh" to Gestures.Oh,
                "OpenEyes" to Gestures.OpenEyes,
                "Roll" to Gestures.Roll,
                "Shake" to Gestures.Shake,
                "Smile" to Gestures.Smile,
                "Surprise" to Gestures.Surprise,
                "Thoughtful" to Gestures.Thoughtful,
                "Wink" to Gestures.Wink
            )

            var remainingMessage = message.trim()
            while (true) {
                val match = gesturePattern.find(remainingMessage)
                if (match != null) {
                    val textPart = remainingMessage.substring(0, match.range.first).trim()
                    if (textPart.isNotEmpty()) {
                        furhat.say(textPart)
                    }

                    val gestureName = match.groupValues[1]
                    gestureMap[gestureName]?.let { gesture ->
                        furhat.gesture(gesture, async = true)
                        Thread.sleep(300)
                    } ?: println("Gesto non riconosciuto: $gestureName")

                    remainingMessage = remainingMessage.substring(match.range.last + 1).trim()
                } else {
                    if (remainingMessage.isNotEmpty()) {
                        furhat.say(remainingMessage)
                    }
                    break
                }
            }

            val response = "Messaggio ricevuto e pronunciato: $message"
            exchange.sendResponseHeaders(200, response.toByteArray().size.toLong())
            exchange.responseBody.use { it.write(response.toByteArray()) }
            return@onEntry
        }
    }
}

class FetchSpeechHandler : HttpHandler {
    override fun handle(exchange: HttpExchange) {
        if (exchange.requestMethod == "GET") {
            println("In attesa di input vocale...")

            // Passiamo l'HttpExchange al contesto della State
            Flow().runAsync(WaitForSpeech(exchange))
        } else {
            exchange.sendResponseHeaders(405, -1)
        }
    }
}

val WaitForSpeech: (HttpExchange) -> State = { exchange ->
    state {
        onEntry {
            furhat.listen(timeout = 5000) // Il tempo prima che furhat dica "sorry I didn't hear you"
        }

        /* The onResponse handler is executed whenever a furhat.listen() or
           furhat.ask() is called and speech is picked up from a user. */
        onResponse {
            val recognizedText = it.text
            println("Testo riconosciuto: $recognizedText")

            // Invia la risposta al client HTTP
            exchange.sendResponseHeaders(200, recognizedText.toByteArray().size.toLong())
            exchange.responseBody.use { os ->
                os.write(recognizedText.toByteArray())
            }
            return@onResponse
        }

        onNoResponse {
            furhat.say("Scusa, non ho sentito nulla. Puoi ripetere?")
            reentry()
        }
    }
}

fun main(args: Array<String>) {
    // System.setProperty("furhatos.skills.brokeraddress", "127.0.0.1")
    System.setProperty("furhatos.skills.brokeraddress", "100.101.0.172")
    Skill.main(args)
}
