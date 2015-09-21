# empty debuginfo
%global debug_package %nil

Name:             snappy-java
Version:          1.0.5
Release:          5%{?dist}
Summary:          Fast compressor/decompresser
License:          ASL 2.0
URL:              http://xerial.org/snappy-java/
Source0:          https://github.com/xerial/snappy-java/archive/%{version}.tar.gz

Patch0:           snappy-java-1.0.5-build.patch

BuildRequires:    libstdc++-static
BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.felix:org.osgi.core)
BuildRequires:    snappy-devel
Requires:         snappy

%description
A Java port of the snappy, a fast compresser/decompresser written in C++.

%package javadoc
Summary:          Javadoc for %{name}
BuildArch:        noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# Cleanup
find -name "*.class" -print -delete
find -name "*.jar" -print -delete

# Remove prebuilt libraries
find -name "*.jnilib" -print -delete
find -name "*.dll" -print -delete
find -name "*.so" -print -delete
find -name "*.h" -print -delete

%patch0 -p1

# Modify pom
%pom_change_dep org.osgi:core org.apache.felix:org.osgi.core
%pom_xpath_remove "pom:dependency[pom:scope = 'test']"
%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:Bundle-NativeCode"

# Unwanted
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-source-plugin

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

chmod 644 NOTICE README.md
sed -i 's/\r//' LICENSE NOTICE README.md

%build
CXXFLAGS="${CXXFLAGS:-%optflags}"
export CXXFLAGS

# no xerial-core package available
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Mon Sep 21 2015 gil cattaneo <puntogil@libero.it> 1.0.5-5
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
