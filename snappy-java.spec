%{?scl:%scl_package snappy-java}
%{!?scl:%global pkg_name %{name}}

# empty debuginfo
%global debug_package %nil

Name:             %{?scl_prefix}snappy-java
Version:          1.1.2.4
Release:          3%{?dist}
Summary:          Fast compressor/decompresser
License:          ASL 2.0
URL:              http://xerial.org/%{pkg_name}/
Source0:          https://github.com/xerial/%{pkg_name}/archive/%{version}.tar.gz
# Not able to build snappy-java jni library with sbt:
# use sbt = 0.13.8 (use scala 2.11.6) available 0.13.1 (use scala 2.10.4)
# Too many missing plugins:
# com.etsy:sbt-checkstyle-plugin:0.4.3
# com.github.gseitz:sbt-release:1.0.0
# com.jsuereth:sbt-pgp:1.0.0
# com.typesafe.sbt:sbt-osgi:0.7.0
# de.johoop:findbugs4sbt:1.4.0
# de.johoop:jacoco4sbt:2.1.5
# org.xerial.sbt:sbt-sonatype:0.5.0
Source1:          http://central.maven.org/maven2/org/xerial/snappy/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Patch0:           %{pkg_name}-1.1.2-build.patch

BuildRequires:    libstdc++-static
BuildRequires:    %{?scl_mvn_prefix}maven-local
BuildRequires:    %{?scl_mvn_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.apache.felix:org.osgi.core)
BuildRequires:    %{?scl_mvn_prefix}mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:    snappy-devel
Requires:         snappy
%{?scl:Requires: %scl_runtime}

%description
A Java port of the snappy, a fast compresser/decompresser written in C++.

%package javadoc
Summary:          Javadoc for %{name}
BuildArch:        noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%{?scl_enable}
%setup -q -n %{pkg_name}-%{version} 
# Cleanup
find -name "*.class" -print -delete
find -name "*.jar" -print -delete
rm -r ./*sbt* project

# Remove prebuilt libraries
find -name "*.jnilib" -print -delete
find -name "*.dll" -print -delete
find -name "*.so" -print -delete
find -name "*.a" -print -delete
find -name "*.h" -print -delete

%patch0 -p1

cp %{SOURCE1} pom.xml
%pom_change_dep org.osgi: org.apache.felix::1.4.0
%pom_xpath_remove "pom:dependency[pom:scope = 'test']"

# Build JNI library
%pom_add_plugin org.apache.maven.plugins:maven-antrun-plugin . '
<dependencies>
 <dependency>
  <groupId>com.sun</groupId>
  <artifactId>tools</artifactId>
  <version>1.8.0</version>
 </dependency>
</dependencies>

<executions>
  <execution>
  <id>compile</id>
  <phase>process-classes</phase>
    <configuration>
      <target>
       <javac destdir="lib"
         srcdir="src/main/java"
         source="1.6" target="1.6" debug="on"
         classpathref="maven.plugin.classpath">
         <include name="**/OSInfo.java"/>
       </javac>
       <exec executable="make">
        <arg line="%{?_smp_mflags}
        JAVA_HOME=%{_jvmdir}/java
        JAVA=%{_jvmdir}/java/bin/java
        JAVAC=%{_jvmdir}/java/bin/javac
        JAVAH=%{_jvmdir}/java/bin/javah"/>
       </exec>
      </target>
    </configuration>
    <goals>
      <goal>run</goal>
    </goals>
  </execution>
</executions>'
# Add OSGi support
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.5.4 . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-Activator>org.xerial.snappy.SnappyBundleActivator</Bundle-Activator>
    <Bundle-ActivationPolicy>lazy</Bundle-ActivationPolicy>
    <Bundle-SymbolicName>${project.groupId}.${project.artifactId}</Bundle-SymbolicName>
    <Bundle-Version>${project.version}</Bundle-Version>
    <Import-Package>org.osgi.framework,*</Import-Package>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

%pom_add_plugin org.apache.maven.plugins:maven-compiler-plugin:3.0 . '
<configuration>
 <source>1.6</source>
 <target>1.6</target>
</configuration>'

chmod 644 NOTICE README.md
# Convert from dos to unix line ending
for file in LICENSE NOTICE README.md; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done
%{?scl_disable}

%build
%{?scl_enable}
CXXFLAGS="${CXXFLAGS:-%optflags}"
export CXXFLAGS
# No test deps available:
#    org.xerial.java:xerial-core:2.1
#    org.xerial:xerial-core:3.2.3
#    org.scalatest:scalatest_2.11:2.2.0
#    com.novocode:junit-interface:0.10
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8
%{?scl_disable}

%install
%{?scl_enable}
%mvn_install
%{?scl_disable}

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Mon Aug 01 2016 Tomas Repik <trepik@redhat.com> - 1.1.2.4-3
- scl conversion

* Mon Jun 20 2016 gil cattaneo <puntogil@libero.it> 1.1.2.4-2
- add missing build requires

* Wed Mar 09 2016 Ricardo Arguello <ricardo@fedoraproject.org> - 1.1.2.4-1
- Update to 1.1.2.4

* Wed Mar 09 2016 gil cattaneo <puntogil@libero.it> - 1.1.2.1-1
- Update to 1.1.2.1

* Mon Sep 21 2015 gil cattaneo <puntogil@libero.it> - 1.0.5-5
- update Url and Source0 fields
- minor changes to adapt to current guideline
- introduce license macro

* Thu Jul 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.5-4
- Build as archful package
- Resolves: rhbz#1245629

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 3 2014 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5
- Use the snappy package instead of a precompiled library

* Mon Mar 31 2014 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.4.1-8
- Switch to XMvn
- Use pom macros

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.4.1-7
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.4.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 4 2012 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.4.1-2
- Cleanup of the spec file

* Tue Feb 21 2012 Marek Goldmann <mgoldman@redhat.com> - 1.0.4.1-1
- Initial packaging
