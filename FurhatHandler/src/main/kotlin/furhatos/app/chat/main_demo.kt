package furhatos.app.chat
/*
import furhatos.flow.kotlin.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.voice.PollyNeuralVoice
import furhatos.flow.kotlin.voice.AcapelaVoice
import furhatos.util.Language


class SimpleSkill : Skill() {
    override fun start() {
        Flow().run(Init)
    }
}

val Init: State = state {
    onEntry {
        //val robotVoice = AcapelaVoice(name = "Samuel22k_HQ", gender = Gender.MALE, language= Language.SWEDISH_FI, rate = 0.8 )
        //furhat.voice = robotVoice
        //furhat.voice = AcapelaVoice(name="Aurora22k_HQ")

        //furhat.say("Ciao! #BIRD# Sono Furhat. Come posso aiutarti?")

        furhat.voice = PollyNeuralVoice(language=Language.ITALIAN)
        furhat.say("Ciao! Sono Furhat. Come posso aiutarti?")

        //goto(Idle)  // Passa a uno stato inattivo dopo aver parlato
    }
}

val Idle: State = state {
    onEntry {
        furhat.say("Sto aspettando un comando.")
    }

    onReentry {
        furhat.say("Se vuoi, possiamo parlare di qualcosa!")
    }
}

fun main(args: Array<String>) {
    //System.setProperty("furhatos.skills.brokeraddress", "100.101.0.172")
    System.setProperty("furhatos.skills.brokeraddress", "127.0.0.1")

    Skill.main(args)
}
*/