package org.pastalab.fray.junit

import org.objectweb.asm.ClassVisitor
import org.objectweb.asm.MethodVisitor
import org.objectweb.asm.Opcodes.ASM9
import org.objectweb.asm.commons.AdviceAdapter

class JunitInstrumenter(cv: ClassVisitor) : ClassVisitor(ASM9, cv) {
    //    "junit/framework/TestCase"
    var shouldInstrument = false

    override fun visit(
        version: Int,
        access: Int,
        name: String,
        signature: String?,
        superName: String?,
        interfaces: Array<out String>?
    ) {
        super.visit(version, access, name, signature, superName, interfaces)
        if (name == "junit/framework/TestCase") {
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

    fun instrumentMethod(
        mv: MethodVisitor,
        access: Int,
        name: String,
        descriptor: String,
        signature: String?,
        exceptions: Array<out String>?
    ): MethodVisitor {
        if (name == "run" && descriptor.startsWith("(Ljunit/framework/TestResult;)V")) {
            return object : AdviceAdapter(ASM9, mv, access, name, descriptor) {
                override fun onMethodEnter() {
                    mv.visitVarInsn(ALOAD, 0)
                    mv.visitMethodInsn(
                        INVOKESTATIC,
                        "org/pastalab/fray/junit/Recorder",
                        "testStart",
                        "(Ljunit/framework/TestCase;)V",
                        false)
                }

                override fun onMethodExit(opcode: Int) {
                    mv.visitVarInsn(ALOAD, 0)
                    mv.visitMethodInsn(
                        INVOKESTATIC,
                        "org/pastalab/fray/junit/Recorder",
                        "testEnd",
                        "(Ljunit/framework/TestCase;)V",
                        false)
                }
            }
        }
        return mv
    }
}
