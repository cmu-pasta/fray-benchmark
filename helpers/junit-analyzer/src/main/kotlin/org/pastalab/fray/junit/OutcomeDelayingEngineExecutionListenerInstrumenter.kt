package org.pastalab.fray.junit

import org.objectweb.asm.ClassVisitor
import org.objectweb.asm.MethodVisitor
import org.objectweb.asm.Opcodes.ASM9
import org.objectweb.asm.Type
import org.objectweb.asm.commons.AdviceAdapter
import org.objectweb.asm.commons.Method

class OutcomeDelayingEngineExecutionListenerInstrumenter(cv: ClassVisitor) :
    ClassVisitor(ASM9, cv)
{
    var shouldInstrument = false
    override fun visit(
        version: Int,
        access: Int,
        name: String?,
        signature: String?,
        superName: String?,
        interfaces: Array<out String>?
    ) {
        super.visit(version, access, name, signature, superName, interfaces)
        if (name == "org/junit/platform/launcher/core/OutcomeDelayingEngineExecutionListener") {
            shouldInstrument = true
        }
    }

    override fun visitMethod(
        access: Int,
        name: String?,
        descriptor: String?,
        signature: String?,
        exceptions: Array<out String>?
    ): MethodVisitor {
        val mv = super.visitMethod(access, name, descriptor, signature, exceptions)
        if (!shouldInstrument) {
            return mv
        }
        return instrumentMethod(mv, access, name!!, descriptor!!, signature, exceptions)
    }
    //            cv, "org.junit.platform.launcher.core.OutcomeDelayingEngineExecutionListener")
    fun instrumentMethod(
        mv: MethodVisitor,
        access: Int,
        name: String,
        descriptor: String,
        signature: String?,
        exceptions: Array<out String>?
    ): MethodVisitor {
        if (name == "executionStarted") {
            return object : AdviceAdapter(ASM9, mv, access, name, descriptor) {
                override fun onMethodEnter() {
                    loadArgs()
                    invokeStatic(
                        Type.getObjectType(Recorder::class.java.name.replace(".", "/")),
                        Method.getMethod("void executionStarted(org.junit.platform.engine.TestDescriptor)"),
                    )
                }
            }
        }
        if (name == "executionFinished") {
            return object : AdviceAdapter(ASM9, mv, access, name, descriptor) {
                override fun onMethodEnter() {
                    loadArgs()
                    invokeStatic(
                        Type.getObjectType(Recorder::class.java.name.replace(".", "/")),
                        Method.getMethod("void executionFinished(org.junit.platform.engine.TestDescriptor, org.junit.platform.engine.TestExecutionResult)"),
                    )
                }
            }
        }
        return mv
    }
}
